import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_talk(message):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": "What is facebook?"}
    ]
  )
  return completion.choices[0].message
def gpt_img():
  completion = openai.Image.create(
    prompt="cute girl",
    n=2,
    size="1024x1024"
  )
  return completion
print(gpt_img())