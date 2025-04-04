import tkinter as tk
from tkinter import messagebox
import json
from career_model import generate_report
import os

# Load questions
with open("questions/questions.json", "r", encoding="utf-8") as f:
    questions_data = json.load(f)

current_question = None
user_responses = []
option_buttons = []
selected_option = None
question_index = 0
selected_field = None
user_name = ""
questions = []

# Start GUI
root = tk.Tk()
root.title("Elevate U - Career Guidance")
root.geometry("600x400")

question_label = tk.Label(root, wraplength=550, justify="left", font=("Arial", 14))
question_label.pack(pady=20)

options_frame = tk.Frame(root)
options_frame.pack()

navigation_frame = tk.Frame(root)
navigation_frame.pack(pady=10)

selected_option_var = tk.StringVar()

def show_question():
    global question_index, questions, selected_option_var, option_buttons

    if 0 <= question_index < len(questions):
        current_question = questions[question_index]
        question_label.config(text=f"Q{question_index + 1}: {current_question['question']}")

        # Set selected option from saved responses
        selected_option_var.set(user_responses[question_index] if user_responses[question_index] else "")

        options = current_question["options"]

        # Create option buttons only once, and reuse them
        while len(option_buttons) < len(options):
            rb = tk.Radiobutton(options_frame, text="", variable=selected_option_var,
                                value="", font=("Arial", 12), anchor="w", justify="left")
            rb.pack(anchor="w", pady=2)
            option_buttons.append(rb)

        # Update buttons with current question's options
        for i, opt in enumerate(options):
            option_buttons[i].config(text=opt, value=opt)
            option_buttons[i].pack(anchor="w")

        # Hide extra buttons (in case previous question had more)
        for i in range(len(options), len(option_buttons)):
            option_buttons[i].pack_forget()

        prev_button.config(state="normal" if question_index > 0 else "disabled")
        next_button.config(text="Next" if question_index < len(questions) - 1 else "Finish")
    else:
        finish_quiz()


def next_question():
    global question_index

    selected = selected_option_var.get()
    if not selected:
        messagebox.showwarning("Selection Required", "Please select an option to proceed.")
        return

    if question_index < len(user_responses):
        user_responses[question_index] = selected
    else:
        user_responses.append(selected)

    if question_index < len(questions) - 1:
        question_index += 1
        show_question()
    else:
        finish_quiz()

def prev_question():
    global question_index

    if question_index > 0:
        question_index -= 1
        show_question()

def finish_quiz():
    global user_name, selected_field, user_responses

    # Ensure all questions are answered
    if len(user_responses) < len(questions) or any(ans == "" for ans in user_responses):
        messagebox.showwarning("Incomplete", "Please answer all questions before finishing.")
        return

    user_data = {
        "name": user_name,
        "field": selected_field,
        "responses": user_responses
    }

    report_path = generate_report(user_data)

    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    show_report(report)

def show_report(report):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Career Report for {report['name']} in {report['field']}", font=("Arial", 14, "bold")).pack(pady=20)
    report_text = tk.Text(root, wrap="word", font=("Arial", 12))
    report_text.insert(tk.END, report["report"])
    report_text.config(state="disabled")
    report_text.pack(padx=20, pady=10, expand=True, fill="both")

def start_quiz():
    global user_name, selected_field, questions, question_index, user_responses

    user_name = name_entry.get().strip()
    selected_field = field_var.get()
    root.bind('<Return>', lambda event: next_question())
    if not user_name:
        messagebox.showwarning("Missing Name", "Please enter your name.")
        return

    if not selected_field or selected_field not in questions_data:
        messagebox.showwarning("Missing Field", "Please select a valid field of interest.")
        return

    questions = questions_data[selected_field]
    question_index = 0
    user_responses = [""] * len(questions)

    for widget in root.winfo_children():
        widget.destroy()

    # UI elements for quiz
    global question_label, options_frame, navigation_frame, selected_option_var, prev_button, next_button

    question_label = tk.Label(root, wraplength=550, justify="left", font=("Arial", 14))
    question_label.pack(pady=20)

    options_frame = tk.Frame(root)
    options_frame.pack()

    navigation_frame = tk.Frame(root)
    navigation_frame.pack(pady=10)

    selected_option_var = tk.StringVar()

    prev_button = tk.Button(navigation_frame, text="Previous", command=prev_question)
    prev_button.grid(row=0, column=0, padx=10)

    next_button = tk.Button(navigation_frame, text="Next", command=next_question)
    next_button.grid(row=0, column=1, padx=10)

    show_question()

# Start screen
tk.Label(root, text="Welcome to Elevate U", font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(root, text="Enter your name:", font=("Arial", 12)).pack()
name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.pack(pady=5)

tk.Label(root, text="Select your career field:", font=("Arial", 12)).pack(pady=10)
field_var = tk.StringVar()
fields_menu = tk.OptionMenu(root, field_var, *questions_data.keys())
fields_menu.config(font=("Arial", 12))
fields_menu.pack()

start_btn = tk.Button(root, text="Start Quiz", font=("Arial", 12), command=start_quiz)
start_btn.pack(pady=20)



root.mainloop()
