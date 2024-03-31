few_shot_examples = [
    {'conversations': [
        {'from': 'User',
        'value': 'Describe the image'},
        {'from': 'Assistant',
        'value': 'Provided is color fundus image of a human retina. The scan seems to exhibit no apparent pathologies or signs of concern, suggesting that it likely belongs to a healthy patient.'},
        {'from': 'User',
        'value': 'Is this case an example of diabetic retinopathy?'},
        {'from': 'Assistant',
        'value': 'The scan does not indicate presence of lesions commonly associated with diabetic retionapthy, such as microaneurysms, hemorrhages or exudates, therefore the patient is unlikely to suffer from any apparent diabetic retinopathy.'}
        ],
        'caption' : 'DR grade: no diabetic retinopathy.',
        'case id' : '20170321103950081'
      },
    {'conversations': [
        {'from': 'User',
        'value': 'This image seems to have a lot going on. Provide some details.'},
        {'from': 'Assistant',
        'value': 'Attached color fundus image appears to contain a wide array of pathologies, indeed suggesting the presence of a serious condition. There are multiple hemorrhages, covering a large area of the posterior pole, as well as multiple yellowish deposits of various diffuse level, likely soft and hard exudates. This leads to conclude that this case is likely an example of severe diabetic retinopathy.'},
        {'from': 'User',
        'value': 'Which stage specifically?'},
        {'from': 'Assistant',
        'value': 'As a virtual assistant I cannot assign a definite diagnosis. However, based on the presence of large area of blood leakage, suggestive of vitreous hemorrhage, this case is likely an example of proliferative diabetic retionapthy, the most severe stage.'},
        {'from' : 'User',
         'value' : 'Should this patient be referred to a doctor?'},
        {'from' : 'Assistant',
         'value' : 'Proliferativx diabetic retionapthy (PDR) is the most serious complication of DR. The patient should likely seek immediate medical help to avoid losing eyesight in the near future.'}
        ],
        'caption' : 'DR grade: proliferative diabetic retinopathy. Present lesions: hard exudates (many, 50+, substantial area coverage), soft exudates (several, 20-30), microaneurysms (many, 50+), hemorrhages (many, 50+, extensive area coverage).',
        'case id' : '007-4204-200'
      },
    {'conversations': [
        {'from': 'User',
        'value': 'This image seems to be of the inside of the eye. Can you tell me anything about what structures we can see?'},
        {'from': 'Assistant',
        'value': 'You are correct! This is a close-up of the retina, the part of the eye responsible for converting light into signals the brain interprets as vision.'},
        {'from': 'User',
        'value': 'It looks pretty normal overall, but there are a couple of tiny, darker spots. Are those important?'},
        {'from': 'Assistant',
        'value': 'That is a good observation. While the image appears mostly healthy, those few dark spots could be microaneurysms. These are basically weak spots in the retinal blood vessels that bulge outward.'},
        {'from' : 'User',
         'value' : 'Should this person be worried?'},
        {'from' : 'Assistant',
         'value' : 'Microaneurysms themselves are not necessarily a cause for immediate alarm, especially since there are only a few visible in this image. However, they can be an early sign of diabetic retinopathy.'},
        {'from' : 'User',
         'value' : 'Diabetic retinopathy? Is there anything else in the image that might suggest that?'},
        {'from' : 'Assistant',
         'value' : 'Not from what I can see here. The absence of other abnormalities like hemorrhages or widespread microaneurysms suggests this might be a very early stage, possibly mild nonproliferative diabetic retinopathy. But remember, I cannot diagnose medical conditions.'}
        ],
        'caption' : 'DR grade: mild nonproliferative diabetic retinopathy. Present lesions: microaneurysms (few, <10).',
        'case id' : '007-1811-100'
      }
 ]