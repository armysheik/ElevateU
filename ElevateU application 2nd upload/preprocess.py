import json
import os

def load_questions(domain):
    """Loads questions for the selected domain."""
    filepath = os.path.join("questions", "questions.json")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError("questions.json not found in the questions/ directory.")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get(domain, [])

def format_for_ai(name, domain, responses):
    """
    Format the prompt for Gemini AI based on the user's name, domain, and answers.
    It pairs each answer with the actual question from the JSON file.
    """
    questions = load_questions(domain)
    if len(questions) != len(responses):
        raise ValueError("Number of responses doesn't match number of questions.")

    prompt = f"""
You are a professional career guidance AI. A student named {name} has taken an interest-based and aptitude questionnaire for the career domain: {domain}.

Here are their responses:
"""
    for idx, (question, answer) in enumerate(zip(questions, responses), 1):
        prompt += f"\nQ{idx}: {question['question']}\nA{idx}: {answer}"

    prompt += """
    
Using the student's answers and domain knowledge of the field, generate a career guidance report that includes:
 start the report with connecting with the student like a human, and avoid bold and give proper spacing for the lines 
1. Matching Percentage: How suitable is the student for this career domain (in %)?
2. Roadmap: What steps should they follow after 12th to succeed in this domain?
3. Future Scope: What is the long-term relevance and growth opportunities in this career?
4. Current Market Demand: What's the demand for this career in India and globally?

Present the report in clear, readable sections with bullet points where needed.
"""
    return prompt.strip()
