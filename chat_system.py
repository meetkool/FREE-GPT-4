import tkinter as tk
from tkinter import ttk
from urllib.parse import urlencode
import requests
from threading import Thread
import subprocess
import time

def start_api_server():
    cmd = "docker container run  -p 4040:5500 d0ckmg/free-gpt4-web-api"
    process = subprocess.Popen(cmd, shell=True)
    time.sleep(5)
    return process

api_process = start_api_server()

def send_message(event=None):
    prompt = entry.get()
    if prompt:
        update_chat_box("User: " + prompt)
        update_chat_box("AI: Loading...")
        entry.delete(0, tk.END)
        progress_bar.start()
        thread = Thread(target=send_request, args=(prompt,))
        thread.start()

def update_chat_box(message):
    chat_box.configure(state=tk.NORMAL)
    chat_box.insert(tk.END, message + "\n")
    chat_box.configure(state=tk.DISABLED)

def send_request(prompt):
    url = "http://127.0.0.1:4040/?" + urlencode({'text': prompt})
    try:
        response = requests.get(url)
        if response.status_code == 200:
            update_chat_box("AI: " + response.text)
        else:
            update_chat_box("Error: Failed to get response from the API.")
    except Exception as e:
        update_chat_box("Error: An unexpected error occurred: " + str(e))
    progress_bar.stop()
    chat_box.yview(tk.END)

def on_enter(event):
    send_button.config(bg="light blue", fg="white")

def on_leave(event):
    send_button.config(bg="SystemButtonFace", fg="black")

window = tk.Tk()
window.title("Chat System")

chat_box = tk.Text(window, state=tk.DISABLED, wrap=tk.WORD)
chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

scrollbar = ttk.Scrollbar(window, command=chat_box.yview)
scrollbar.grid(row=0, column=2, sticky="ns")
chat_box.configure(yscrollcommand=scrollbar.set)

entry = tk.Entry(window)
entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

send_button = tk.Button(window, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

window.bind('<Return>', send_message)

send_button.bind("<Enter>", on_enter)
send_button.bind("<Leave>", on_leave)

style = ttk.Style()
style.configure("TProgressbar", thickness=20)
progress_bar = ttk.Progressbar(window, style="TProgressbar", mode="indeterminate")
progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

entry.focus()

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

window.mainloop()

 api_process.terminate()
