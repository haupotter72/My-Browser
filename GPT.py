import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_talk(message):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": f"What is {message}?"}
    ]
  )
  return completion.choices[0].message.content

def gpt_gen_img(text):
  image_resp = openai.Image.create(
    prompt=text, n=1, size="512x512")
  print(image_resp)
  return image_resp.data[0].url