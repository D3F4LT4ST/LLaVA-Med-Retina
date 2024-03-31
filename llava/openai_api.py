import openai
import time
import asyncio
import os

openai.api_key = os.environ['OPENAI_API_KEY']

async def dispatch_openai_requests(
  model,
  messages_list,
  temperature,
):
    async_responses = [
        openai.ChatCompletion.acreate(
            model=model,
            messages=x,
            temperature=temperature,
        )
        for x in messages_list
    ]
    return await asyncio.gather(*async_responses)


def call_async(samples, wrap_gen_message, model, print_result=False):
  message_list = []
  for sample in samples:
    input_msg = wrap_gen_message(sample)
    message_list.append(input_msg)
  
  try:
    predictions = asyncio.run(
      dispatch_openai_requests(
        model=model,
        messages_list=message_list,
        temperature=0.0,
      )
    )
  except Exception as e:
    print(f"Error in call_async: {e}")
    time.sleep(6)
    return []

  results = []
  for sample, prediction in zip(samples, predictions):
    if prediction:
      if 'content' in prediction['choices'][0]['message']:
        sample['result'] = prediction['choices'][0]['message']['content']
        if print_result:
          print(sample['result'])
        results.append(sample)
  return results