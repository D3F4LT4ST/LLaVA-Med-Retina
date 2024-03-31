import sys
import time
import json
import argparse
import numpy as np
from tqdm import tqdm

from instruct_few_shot_examples import few_shot_examples

sys.path.append("llava")
from openai_api import call_async

conv_to_str = lambda conv: "\n\n".join([("User: " if x["from"] == "human" else "Assistant: ") + x["value"] for x in conv])

class PromptGenerator:

  @staticmethod
  def few_shot_messages_gen(query_context):
    messages = [
    {
      "role": "system", "content": """You are an AI assistant specialized in biomedical topics, specifically ophthalmology.

  You are provided with a text description (Figure Caption) of a color fungus image. The field of view captures the entire area of the posterior pole, so you can assume the optic disk, macular area and major blood vessels are all visible. The description states whether the signs of diabetic retinopathy (DR) are observed in the image, as well as the disease grade, if applicable. Presence and properties of particular lesions associated with the disease may also be indicated. Unfortunately, you do not have access to the image itself.

  Your task is to generate a conversation between a person (User) inquiring about the image and you (Assistant) responding to their questions. The conversation should proceed as though both the User and Assistant are viewing the image, while not referring to the text information (Figure Caption). 

  Below are requirements for generating the questions and answers in the conversation:
  - Remain restricted to the information provided in the caption. I.e you must not suggest the presence of certain lesions typically associated with the disease if they are not explicitly mentioned in the description.
  - Do not use phrases like "mentioned", "caption", "context" in the conversation. Instead, refer to the information as being "in the image."
  - You are encouraged to use the terminology associated with diabetic retinopathy to describe different outlined lesions and generate rich conversations.
  - Ensure that questions are diverse and cover a range of visual aspects of the image. This can also include generic inquires about the image.
  - The conversation should include at least 3-4 turns of questions and answers about the visual aspects of the image (3-4 if the caption contains descriptions of present lesions). If the image states the grade of the disease, the conversation must involve at least one inquiry from the user regarding the severity of the condition.
  - Answer responsibly, avoiding overconfidence, and providing direct medical advise. Encourage the user to consult a healthcare professional for advice.
  """},
    ]
    for ex in few_shot_examples:
      messages += [
        {"role": "user", "content": PromptGenerator.context_gen(ex)},
        {"role": "assistant", "content": conv_to_str(ex["conversations"])},
      ]
    messages.append({"role": "user", "content": query_context})
    return messages

  @staticmethod
  def context_gen(sample):
    return f"Figure Caption:\n: {sample['caption']}"

  @staticmethod
  def wrap_gen_message(sample):
    text = PromptGenerator.context_gen(sample)
    context = PromptGenerator.few_shot_messages_gen(text)
    return context


def main(args):
  with open(args.input_path) as f:
    captions = json.load(f) 

  results = []
  for batch in tqdm(np.split(np.array(captions), args.num_batches)):
        
      async_results = call_async(list(batch), lambda x: PromptGenerator.wrap_gen_message(x), args.model)
      results.extend(async_results)
      time.sleep(args.delay)

  with open(args.output_path, 'w') as f:
    json.dump(results, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str)
    parser.add_argument('--output_path', type=str)
    parser.add_argument('--model', type=str)
    parser.add_argument('--num_batches', type=int)
    parser.add_argument('--delay', type=float)
    args = parser.parse_args()
    main(args)