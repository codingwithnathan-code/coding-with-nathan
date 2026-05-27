import tkinter as tk
from tkinter import messagebox
import json
import os

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
SUCCESS_COLOR = "#2ECC71"  # Green
DELETE_COLOR = "#E74C3C"  # Red
TEXT_COLOR = "#ECF0F1"


class TodoListApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To-Do List - Coding With Nathan")
        self.root.geometry("700x600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # File to save tasks
        self.data_file = "tasks.json"
        self.tasks = []  # List to store tasks

        self.create_widgets()
        self.load_tasks()  # Load saved tasks when app starts

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="My To-Do List",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=20)

        # Add Task Frame
        add_frame = tk.Frame(self.root, bg=BG_COLOR)
        add_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(
            add_frame, text="New Task:", font=("Arial", 12), bg=BG_COLOR, fg=LABEL_COLOR
        ).pack(side=tk.LEFT, padx=5)

        self.task_entry = tk.Entry(add_frame, font=("Arial", 14), width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5, expand=True, fill="x")
        self.task_entry.bind(
            "<Return>", lambda e: self.add_task()
        )  # Press Enter to add

        add_button = tk.Button(
            add_frame,
            text="Add Task",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            command=self.add_task,
        )
        add_button.pack(side=tk.LEFT, padx=5)

        # Task Listbox
        list_frame = tk.Frame(self.root, bg=BG_COLOR)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 12),
            height=15,
            bg="#34495E",
            fg=TEXT_COLOR,
            selectbackground=ACCENT_COLOR,
        )
        self.task_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=15)

        complete_btn = tk.Button(
            btn_frame,
            text="Mark Complete",
            font=("Arial", 11, "bold"),
            bg=SUCCESS_COLOR,
            fg="white",
            width=15,
            command=self.mark_complete,
        )
        complete_btn.pack(side=tk.LEFT, padx=8)

        delete_btn = tk.Button(
            btn_frame,
            text="Delete Task",
            font=("Arial", 11, "bold"),
            bg=DELETE_COLOR,
            fg="white",
            width=15,
            command=self.delete_task,
        )
        delete_btn.pack(side=tk.LEFT, padx=8)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear All",
            font=("Arial", 11, "bold"),
            bg="#95A5A6",
            fg="white",
            width=12,
            command=self.clear_all,
        )
        clear_btn.pack(side=tk.LEFT, padx=8)

        # Status
        self.status_label = tk.Label(
            self.root, text="0 tasks", font=("Arial", 10), bg=BG_COLOR, fg="gray"
        )
        self.status_label.pack(pady=10)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Empty Task", "Please enter a task!")

    def mark_complete(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = True
            self.update_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning(
                "No Selection", "Please select a task to mark as complete."
            )

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_listox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to delete.")

    def clear_all(self):
        if messagebox.askyesno(
            "Clear All", "Are you sure you want to delete all tasks?"
        ):
            self.tasks.clear()
            self.update_listbox()
            self.save_tasks()

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = task["task"]
            if task["completed"]:
                display_text = "✔️ " + display_text
            self.task_listbox.insert(tk.END, display_text)

        # Update status
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        self.status_label.config(text=f"{completed}/{total} tasks completed")

    def save_tasks(self):
        try:
            with open(self.data_file, "w") as file:
                json.dump(self.tasks, file)
        except Exception:
            print("Could not save tasks.")

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as file:
                    self.tasks = json.load(file)
                self.update_listbox()
            except Exception:
                self.tasks = []

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = TodoListApp()
    app.run()
