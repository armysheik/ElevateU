import tkinter as tk
from tkinter import messagebox
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Load questions
with open("data/questions.json", "r", encoding="utf-8") as f:
    question_data = json.load(f)

# Flatten questions with categories
questions = []
for category, subcategories in question_data.items():
    for subcategory, q_list in subcategories.items():
        for q in q_list:
            q["category"] = category.replace("_", " ").title()  # Store category name
            questions.append(q)

# Initialize variables
current_question_index = 0
user_name = ""
user_answers = {}

# Create main GUI
root = tk.Tk()
root.title("Career Guidance Test")
root.geometry("600x500")

frame = tk.Frame(root)
frame.pack(pady=20)

name_label = tk.Label(frame, text="Enter your name:", font=("Arial", 14))
name_label.pack()

name_entry = tk.Entry(frame, font=("Arial", 14))
name_entry.pack(pady=5)

start_button = tk.Button(frame, text="Start Test", font=("Arial", 14), command=lambda: start_test())
start_button.pack(pady=10)

question_frame = tk.Frame(root)

question_label = tk.Label(question_frame, text="", wraplength=500, font=("Arial", 14))
question_label.pack()

category_label = tk.Label(question_frame, text="", font=("Arial", 12, "italic"))
category_label.pack(pady=5)

options_var = tk.StringVar()
options_buttons = []

def start_test():
    global user_name
    user_name = name_entry.get().strip()
    if not user_name:
        messagebox.showerror("Error", "Please enter your name.")
        return

    frame.pack_forget()
    question_frame.pack(pady=20)
    show_question()

def show_question():
    global current_question_index

    if current_question_index >= len(questions):
        generate_ai_report()
        return

    q_data = questions[current_question_index]
    question_label.config(text=q_data["question"])
    category_label.config(text=f"Category: {q_data['category']}")

    options_var.set(None)
    
    for btn in options_buttons:
        btn.destroy()
    
    options_buttons.clear()

    for option in q_data["options"]:
        btn = tk.Radiobutton(question_frame, text=option, variable=options_var, value=option, font=("Arial", 12))
        btn.pack(anchor="w", padx=20, pady=2)
        options_buttons.append(btn)

    next_button.pack(pady=10)
    prev_button.pack(pady=5) if current_question_index > 0 else prev_button.pack_forget()

def next_question():
    global current_question_index
    selected_option = options_var.get()

    if not selected_option:
        messagebox.showerror("Error", "Please select an option before proceeding.")
        return

    user_answers[current_question_index] = selected_option
    current_question_index += 1
    show_question()

def prev_question():
    global current_question_index
    if current_question_index > 0:
        current_question_index -= 1
        show_question()

next_button = tk.Button(question_frame, text="Next", font=("Arial", 14), command=next_question)
prev_button = tk.Button(question_frame, text="Previous", font=("Arial", 14), command=prev_question)

root.bind("<Return>", lambda event: next_question())  # Press Enter to go to next question

# ---- AI Integration ----
def generate_ai_report():
    """Send user answers to Gemini API and get a career recommendation."""
    messagebox.showinfo("Test Completed", f"Thank you {user_name}! Generating your career report...")

    # Prepare prompt for AI
    user_responses_text = "\n".join([f"Q{i+1}: {questions[i]['question']}\nUser Answer: {answer}" for i, answer in user_answers.items()])

    prompt = f"""
    You are an expert career counselor. Analyze the user's responses and provide a detailed career guidance report. 
    Consider the cognitive abilities, personality traits, career interests, and emotional factors.
    
    User Name: {user_name}
    Responses:
    {user_responses_text}

    Based on the responses, suggest the top 3 career fields that best suit the user.
    Provide a brief explanation for each recommendation.
    """

    try:
        response = model.generate_content(prompt)
        ai_report = response.text  # Get AI-generated career guidance
        
        # Show AI-generated career report in a new window
        show_ai_report(ai_report)

    except Exception as e:
        messagebox.showerror("Error generating report", str(e))

def show_ai_report(report):
    """Display AI-generated career report in a pop-up window."""
    report_window = tk.Toplevel(root)
    report_window.title("Career Report")
    report_window.geometry("600x400")

    report_label = tk.Label(report_window, text="Career Guidance Report", font=("Arial", 16, "bold"))
    report_label.pack(pady=10)

    report_text = tk.Text(report_window, wrap="word", font=("Arial", 12))
    report_text.insert("1.0", report)
    report_text.pack(padx=10, pady=5, expand=True, fill="both")

    close_button = tk.Button(report_window, text="Close", font=("Arial", 14), command=report_window.destroy)
    close_button.pack(pady=10)

root.mainloop()
