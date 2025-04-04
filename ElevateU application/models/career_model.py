import os
import google.generativeai as genai
from dotenv import load_dotenv
from preprocess import format_for_gemini

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_career_recommendation(user_data):
    prompt = format_for_gemini(user_data)
    response = model.generate_content(prompt)
    return response.text  # returning plain string is fine
 