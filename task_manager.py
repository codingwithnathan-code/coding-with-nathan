import tkinter as tk
from tkinter import messagebox, ttk
import json
import datetime
import os

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
SUCCESS_COLOR = "#2ECC71"  # Green
OVERDUE_COLOR = "#E74C3C"  # Red
TEXT_COLOR = "#ECF0F1"
WARNING_COLOR = "#E74C3C"  # Red


class TaskManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Personal Task Manager - Coding With Nathan")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)

        self.data_file = "tasks.json"
        self.tasks = []
        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="✅ Personal Task Manager",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=15)

        # Add Task Frame
        add_frame = tk.Frame(self.root, bg=BG_COLOR)
        add_frame.pack(pady=10, padx=40, fill="x")

        tk.Label(add_frame, text="Task:", bg=BG_COLOR, fg=LABEL_COLOR).pack(
            side=tk.LEFT
        )
        self.task_entry = tk.Entry(add_frame, font=("Arial", 12), width=40)
        self.task_entry.pack(side=tk.LEFT, padx=10)

        tk.Label(
            add_frame, text="Due Date (YYYY-MM-DD):", bg=BG_COLOR, fg=LABEL_COLOR
        ).pack(side=tk.LEFT, padx=10)
        self.due_entry = tk.Entry(add_frame, font=("Arial", 12), width=15)
        self.due_entry.pack(side=tk.LEFT)

        add_btn = tk.Button(
            add_frame,
            text="Add Task",
            font=("Arial", 11, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            command=self.add_task,
        )
        add_btn.pack(side=tk.LEFT, padx=10)

        # Task List
        list_frame = tk.Frame(self.root, bg=BG_COLOR)
        list_frame.pack(pady=10, padx=40, fill="both", expand=True)

        columns = ("Task", "Due Date", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Status", text="Status")

        self.tree.column("Task", width=400)
        self.tree.column("Due Date", width=120)
        self.tree.column("Status", width=100)

        self.tree.pack(fill="both", expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        complete_btn = tk.Button(
            btn_frame,
            text="Mark Complete",
            font=("Arial", 11),
            bg=SUCCESS_COLOR,
            fg="white",
            command=self.mark_complete,
        )
        complete_btn.pack(side=tk.LEFT, padx=10)

        delete_btn = tk.Button(
            btn_frame,
            text="Delete Task",
            font=("Arial", 11),
            bg=WARNING_COLOR,
            fg="white",
            command=self.delete_task,
        )
        delete_btn.pack(side=tk.LEFT, padx=10)

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.tasks = json.load(f)
                self.refresh_tree()
            except:
                self.tasks = []

    def save_tasks(self):
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.tasks, f, indent=2)
        except:
            pass

    def add_task(self):
        task_text = self.task_entry.get().strip()
        due_date = self.due_entry.get().strip()

        if not task_text:
            messagebox.showwarning("Missing Info", "Task description is required!")
            return

        try:
            # Validate date format
            datetime.datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid Date", "Please use YYYY-MM-DD format!")
            return

        self.tasks.append({"task": task_text, "due_date": due_date, "completed": False})

        self.save_tasks()
        self.refresh_tree()

        # Clear fields
        self.task_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)

    def refresh_tree(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        today = datetime.date.today()

        for task in self.tasks:
            due = datetime.datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            status = (
                "Completed"
                if task["completed"]
                else ("Overdue" if due < today else "Pending")
            )

            tag = (
                "completed"
                if task["completed"]
                else ("overdue" if due < today else "normal")
            )

            self.tree.insert(
                "", "end", values=(task["task"], task["due_date"], status), tags=(tag,)
            )

            # Configure tags for colors
            self.tree.tag_configure("completed", foreground="gray")
            self.tree.tag_configure("overdue", foreground=WARNING_COLOR)

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task!")
            return

        index = self.tree.index(selected[0])
        self.tasks[index]["completed"] = True
        self.save_tasks()
        self.refresh_tree()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task!")
            return

        if messagebox.askyesno("Delete", "Delete this task?"):
            index = self.tree.index(selected[0])
            del self.tasks[index]
            self.save_tasks()
            self.refresh_tree()

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = TaskManager()
    app.run()
