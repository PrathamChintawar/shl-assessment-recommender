import google.generativeai as genai

from app.config import GEMINI_API_KEY
from app.config import LLM_MODEL

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(LLM_MODEL)


def generate(prompt: str):

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        print(e)

        return (
            "I'm unable to generate a response at the moment."
        )