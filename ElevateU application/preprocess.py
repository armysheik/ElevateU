def format_for_gemini(user_data):
    name = user_data.get("name", "Student")
    responses = user_data.get("responses", [])

    formatted = f"Career guidance report for {name}.\n\nBased on the user's responses:\n"
    for i, response in enumerate(responses, start=1):
        question = response.get("question", "")
        answer = response.get("answer", "")
        formatted += f"{i}. Q: {question}\n   A: {answer}\n"

    formatted += "\nProvide a career recommendation based on the answers above. Mention potential career paths, reasoning, and strengths."
    return formatted
