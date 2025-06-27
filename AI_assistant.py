# Setup
import tkinter as tk
from tkinter import messagebox
import requests
from io import BytesIO
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

#Contents
APP_TITLE = "AI Assistant developed by Iqra Arif"
WINDOW_SIZE = "900x750"
BG_COLOR = "#F5F5F5"
FONT_AI = ("Geogia", 22 , "bold")
FONT_SUB =("Palatino Linotype" , 18 , "bold")
TEXT_COLOR = "#000000"
INPUT_BG = "#9AB9D8"
BTN_COLOR = "#22C55E"
BTN_HOVER = "#6C757D"
FONT_MAIN = ("Tahoma",13)
FONT_LOG =("Consolas", 11 , "bold")

#Validate Student IDs(Range 0001 to 0100)
VALID_IDS = [f"{i:03}"for i in range(0 , 93)]

#Button hover effects
def on_enter(e):
    generate_btn.config(bg=BTN_HOVER)

def on_leave(e):
    generate_btn.config(bg=BTN_COLOR)

def validate_student_id(sid):
    return sid in VALID_IDS

def log_message(message):
    log_output.config(state=tk.NORMAL)
    log_output.insert(tk.END, message + "\n")
    log_output.see(tk.END) 
    log_output.config(state=tk.DISABLED)

def call_gemini_api(student_id, question):
    try:
        prompt = f"Student ID: {student_id}. Question : {question}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"
    
def generate_script():
    student_id = student_id_entry.get().strip()
    question = question_input.get("1.0", tk.END).strip()

    if not validate_student_id(student_id):
        messagebox.showerror("Invalid ID", "Student ID must be between 001 and 092.")
        return
    
    if not question:
        messagebox.showerror("Missing Question", "Please enter your question.")
        return
    
    log_message(f"Asking for student ID {student_id}...\n {question}")
    response = call_gemini_api(student_id, question)
    log_message(f"Response:\n{response}")

#GUI Setup

app = tk.Tk()
app.title(APP_TITLE)
app.geometry(WINDOW_SIZE)
app.configure(bg=BG_COLOR)

# Title section
title_frame = tk.Frame(app, bg=BG_COLOR)
title_frame.pack(pady=(10, 0))

ai_label = tk.Label(title_frame, text="AI", font=FONT_AI, fg="blue", bg=BG_COLOR)
ai_label.pack(side=tk.LEFT) 
assistant_label = tk.Label(title_frame, text="Assistant", font=FONT_AI, fg="blue", bg=BG_COLOR)
assistant_label.pack(side=tk.LEFT)

sub_label = tk.Label(app, text="developed by Iqra Arif",font=FONT_SUB, fg="black", bg=BG_COLOR)
sub_label.pack(pady=(0, 20))

main_frame = tk.Frame(app, bg=BG_COLOR)
main_frame.pack(fill=tk.BOTH, expand=True)

#ID input
tk.Label(main_frame, text="Enter Student ID(001 to 092):",font=FONT_MAIN, bg=BG_COLOR).pack(anchor="w",padx=40)
student_id_entry = tk.Entry(main_frame, font=FONT_MAIN, bg=INPUT_BG,fg=TEXT_COLOR)
student_id_entry.pack(fill=tk.X,padx=40, pady=(0, 20))

#Question input
tk.Label(main_frame, text="Enter your question:",font=FONT_MAIN, bg=BG_COLOR).pack(anchor="w",padx=40)
question_input = tk.Text(main_frame, height=7, font=FONT_MAIN, bg=INPUT_BG,fg=TEXT_COLOR)
question_input.pack(fill=tk.X,padx=40, pady=(0, 20))
 
#Send button
generate_btn = tk.Button(main_frame, text="Send", font=("Courier New", 13, "bold"),
                         bg=BTN_COLOR,fg="white", relief=tk.FLAT,command=generate_script)
generate_btn.pack(pady=(0, 20),ipadx=10)
generate_btn.bind("<Enter>", on_enter)
generate_btn.bind("<Leave>", on_leave)

#Log section
tk.Label(main_frame, text="Conversation Log:", font=("Courier New", 13, "bold"),
         fg="darkblue", bg=BG_COLOR).pack(anchor="w",padx=40)

log_output = tk.Text(main_frame, height=13, font=FONT_LOG, bg="#E5E7EB",
                  fg="#000000",state=tk.DISABLED, wrap=tk.WORD)
log_output.pack(fill=tk.BOTH, padx=40, pady=(5, 20),expand=True)

app.mainloop()