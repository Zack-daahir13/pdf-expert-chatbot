import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

def get_chat_response(question, context):
    prompt = f"""Context: {context}\n\nQuestion: {question}"""
    response = model.generate_content(prompt)
    return response.text
