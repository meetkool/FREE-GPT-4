import tkinter as tk
from tkinter import ttk
import requests
from threading import Thread

# Colors
BG_COLOR = "#f5f5f5"  # Light gray
TEXT_COLOR = "#333333"  # Dark gray
USER_COLOR = "#007bff"  # Blue
AI_COLOR = "#28a745"  # Green
ERROR_COLOR = "#dc3545"  # Red

# Fonts
FONT_FAMILY = "Arial"
FONT_SIZE = 10

def send_message(event=None):
    prompt = entry.get()
    if prompt:
        # Display user message
        chat_box.configure(state=tk.NORMAL)
        chat_box.insert(tk.END, "User: " + prompt + "\n", "user")
        chat_box.configure(state=tk.DISABLED)

        # Clear the entry field
        entry.delete(0, tk.END)

        # Start loading animation
        progress_bar.start()

        # Start typing animation
        typing_label.config(text="AI is typing...", fg=AI_COLOR)

        # Send request in a separate thread
        thread = Thread(target=send_request, args=(prompt,))
        thread.start()

def send_request(prompt):
    url = "http://127.0.0.1:4040/?text=" + prompt
    response = requests.get(url)
    if response.status_code == 200:
        # Update chat box with API response
        chat_box.configure(state=tk.NORMAL)
        chat_box.insert(tk.END, "AI: " + response.text + "\n", "ai")
        chat_box.configure(state=tk.DISABLED)
    else:
        chat_box.configure(state=tk.NORMAL)
        chat_box.insert(tk.END, "Error: Failed to get response from the API.\n", "error")
        chat_box.configure(state=tk.DISABLED)

    # Stop loading animation
    progress_bar.stop()

    # Stop typing animation
    typing_label.config(text="")

    # Scroll to the end of the chat history
    chat_box.yview(tk.END)

def on_enter(event):
    send_button.config(bg="#007bff", fg="white")

def on_leave(event):
    send_button.config(bg="white", fg="#333333")

# Create the main window
window = tk.Tk()
window.title("Chat System")
window.configure(bg=BG_COLOR)

# Create a frame for the chat history and scrollbar
chat_frame = ttk.Frame(window)
chat_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Configure grid weights for chat_frame
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# Create a text box to display the chat history
chat_box = tk.Text(chat_frame, state=tk.DISABLED, wrap=tk.WORD, bg=BG_COLOR, fg=TEXT_COLOR)
chat_box.grid(row=0, column=0, sticky="nsew")
chat_box.tag_configure("user", foreground=USER_COLOR)
chat_box.tag_configure("ai", foreground=AI_COLOR)
chat_box.tag_configure("error", foreground=ERROR_COLOR)

# Create a scrollbar for the chat box
scrollbar = ttk.Scrollbar(chat_frame, command=chat_box.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
chat_box.configure(yscrollcommand=scrollbar.set)

# Set the minimum size for chat_frame
chat_frame.grid_columnconfigure(0, weight=1)
chat_frame.grid_rowconfigure(0, weight=1)


# Create an entry field for user input
entry = tk.Entry(window, bg="white", fg="#333333", font=(FONT_FAMILY, FONT_SIZE))
entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

# Create a button to send messages
send_button = tk.Button(window, text="Send", command=send_message, bg="#007bff", fg="white", font=(FONT_FAMILY, FONT_SIZE))
send_button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="e")

# Bind Enter key press to send_message function
window.bind('<Return>', send_message)

# Configure hover effects for the send button
send_button.bind("<Enter>", on_enter)
send_button.bind("<Leave>", on_leave)

# Create a progress bar for loading animation
style = ttk.Style()
style.configure("TProgressbar", thickness=20)
progress_bar = ttk.Progressbar(window, style="TProgressbar", mode="indeterminate")
progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Create a label for typing animation
typing_label = tk.Label(window, text="", font=(FONT_FAMILY, FONT_SIZE), bg=BG_COLOR, fg=AI_COLOR)
typing_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Set focus to the entry field
entry.focus()

# Configure grid weights to make the chat box expandable
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# Run the main event loop
window.mainloop()
