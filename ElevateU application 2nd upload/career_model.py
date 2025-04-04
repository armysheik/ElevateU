import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from preprocess import format_for_ai

# Load .env to get the API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_report(user_data):
    """
    Generates a career guidance report using Gemini AI based on user responses.
    Saves the report as a JSON file in the 'responses/' folder.
    """
    name = user_data["name"]
    field = user_data["field"]
    responses = user_data["responses"]

    # Format prompt for AI
    prompt = format_for_ai(name, field, responses)
    
    try:
        response = model.generate_content(prompt)
        report_text = response.text
    except Exception as e:
        report_text = f"An error occurred while generating the report: {str(e)}"

    # Save report
    report = {
        "name": name,
        "field": field,
        "report": report_text
    }

    os.makedirs("responses", exist_ok=True)
    report_file = f"responses/{name}_report.json"

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report_file
