import os
import scipy
import json
import cv2
import argparse
import PIL.Image
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm

LESION_NAME_MAP = {
    'he' : 'hemorrhages',
    'ex' : 'hard exudates',
    'se' : 'soft exudates',
    'ma' : 'microaneurysms'
}

GRADE_MAP = {
    0: 'no diabetic retinopathy',
    1: 'mild nonproliferative diabetic retinopathy',
    2: 'moderate nonproliferative diabetic retinopathy',
    3: 'severe nonproliferative diabetic retinopathy',
    4: 'proliferative diabetic retinopathy'
}

LESION_QUANTITY_MAP = lambda n: 'few, <10' if n <= 10 else ('several, 20-30' if n <= 50 else 'many, 50+')

LESION_COVERAGE_MAP = lambda area: '' if area < 10000000 else ('substantial area coverage' if area < 50000000 else 'extensive area coverage')

def get_lesion_stats(args, case):
    
    detection_label_path = f'{args.input_path}/lesion_detection/{case["set"]}/{case["case id"]}.xml'
    
    tree = ET.parse(detection_label_path)
    root = tree.getroot()
    
    lesion_count = {}
    for obj in root.findall('object'):
        lesion_name = obj.find('name').text
        
        lesion_count.setdefault(lesion_name, 0)
        lesion_count[lesion_name] += 1
        
    lesion_coverage = {}
    for lesion_name in LESION_NAME_MAP:
        lesion_coverage.setdefault(lesion_name, 0)
        
        segmentation_mask_path = f'{args.input_path}/lesion_segmentation/{case["set"]}/label/{lesion_name.upper()}/{case["case id"]}.tif'
        if not os.path.exists(segmentation_mask_path): continue
        
        mask = np.array(PIL.Image.open(segmentation_mask_path).convert('L'))
        lesion_coverage[lesion_name] = mask.sum()
            
    return lesion_count, lesion_coverage

def create_captions(args, cases):
    
    captions = []
    for i in tqdm(range(len(cases))):
        case = cases.iloc[i]
        caption = ''
        if not np.isnan(case['grade']):
            caption += f'DR grade: {GRADE_MAP[int(case["grade"])]}' + '.'
        if not np.isnan(case['annotated']):
            lesion_count, lesion_coverage = get_lesion_stats(args, case)
            if caption: caption += ' '
            caption += f'Present lesions: ' + ', '.join([
                f'{LESION_NAME_MAP[lesion]} ({LESION_QUANTITY_MAP(lesion_count[lesion])}' +  
                (f', {LESION_COVERAGE_MAP(lesion_coverage[lesion])}' if LESION_COVERAGE_MAP(lesion_coverage[lesion]) else '') + ')'
                for lesion in lesion_count
            ]) + '.'
    
        captions.append({
            'caption' : caption,
            'case id': case["case id"],
            'rich' : not np.isnan(case['grade']) and not np.isnan(case['annotated'])
        })
    
    with open(f'{args.output_path}/ddr_qa_captions.json', 'w') as f:
        json.dump(captions, f)


def preprocess_images(args, cases):
    
    if not os.path.exists(f'{args.output_path}/images'):
        os.makedirs(f'{args.output_path}/images')
    
    for i in tqdm(range(len(cases))):
        case = cases.iloc[i]
        
        category = 'DR_grading' if np.isnan(case['annotated']) else 'lesion_segmentation'
        subfolder = 'image' if category == 'lesion_segmentation' else ''
        
        img = PIL.Image.open(f'{args.input_path}/{category}/{case["set"]}/{f"{subfolder}/" if subfolder else ""}{case["case id"]}.jpg')
        img_gray = img.convert('L')
        w,h = img.size
        
        img_gray_small = cv2.GaussianBlur(np.array(img_gray.resize((int(w / h * 128), 128))), (5,5),3)
        
        bg_value = scipy.stats.mode(img_gray_small.ravel(), keepdims=False).mode
    
        img = np.pad(np.array(img), ((1,1), (1,1), (0,0)))
        img_gray = np.pad(np.array(img_gray), ((1,1), (1,1)))

        _, img_bin = cv2.threshold(img_gray, bg_value+10, 255, 0)
        contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
        max_contour = max(contours, key=lambda contour: cv2.contourArea(contour))
        [bound_x, bound_y, bound_w, bound_h] = cv2.boundingRect(max_contour)
        
        img_crop = img[bound_y:bound_y+bound_h, bound_x:bound_x+bound_w]
        
        if bound_h > bound_w:
            padding = ((0,0), ((bound_h-bound_w)//2, (bound_h-bound_w)//2), (0,0))
        else:
            padding = (((bound_w-bound_h)//2, (bound_w-bound_h)//2), (0,0), (0,0))
        img_crop = PIL.Image.fromarray(np.pad(img_crop, padding))
        
        w,h = img_crop.size
        
        img_crop_downscaled = img_crop.resize((int(w / h * 512), 512), resample=PIL.Image.BILINEAR)
        
        img_crop_downscaled.save(f'{args.output_path}/images/{case["case id"]}.jpg')
                     

def main(args):

    graded_cases = pd.read_csv(f'{args.input_path}/DR_grading/train.txt', delimiter=' ', names=['case id', 'grade'])
    graded_cases['set'] = 'train'
    graded_cases['case id'] = graded_cases['case id'].apply(lambda case: case[:-4])
    graded_cases = graded_cases[graded_cases['grade'] != 5]

    annotated_cases = pd.concat([
        pd.DataFrame(
            {'case id' : os.listdir(f'{args.input_path}/lesion_detection/{set_}'), 'annotated' : True, 'set': set_}
        ).apply(lambda case: (case[0][:-4], case[1], case[2]), axis=1, result_type='broadcast')
        for set_ in ['train', 'valid', 'test']
    ])

    all_cases = pd.merge(graded_cases, annotated_cases, on=['case id', 'set'], how='outer')

    preprocess_images(args, all_cases)
    create_captions(args, all_cases)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str)
    parser.add_argument('--output_path', type=str)
    args = parser.parse_args()

    main(args)
