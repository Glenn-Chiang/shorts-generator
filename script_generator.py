import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, GenerationConfigType
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

generation_config: GenerationConfigType = {
    'temperature': 1
}


def generate_script():
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    with open('prompt.txt', 'r') as prompt_file:
        prompt = prompt_file.read()

    try:
        response = model.generate_content(
            prompt, safety_settings=safety_settings, generation_config=generation_config)
        response_text = response.text
        return json.loads(response_text)

    except Exception as error:
        print("Error generating response: ", error)
        return


if __name__ == '__main__':
    script = generate_script()
    # print(script)
    print(script['title'])
    print(script['content'])
    # print(script['sentences'])
    print(script['keywords'])
