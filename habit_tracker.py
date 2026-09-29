import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import date, datetime, timedelta

# ==================== COLORS ====================
BG_COLOR = "#1e1e2e"
TITLE_COLOR = "#cdd6f4"
TEXT_COLOR = "#cdd6f4"
ACCENT_COLOR = "#89b4fa"
SUCCESS_COLOR = "#a6e3a1"
WARNING_COLOR = "#f9e2af"
DANGER_COLOR = "#f38ba8"
BUTTON_COLOR = "#313244"
CARD_BG = "#181825"

SAVE_FILE = "habits.json"


class HabitTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Habit Tracker - Coding With Nathan")
        self.root.geometry("740x760")
        self.root.configure(bg=BG_COLOR)

        self.habits = []
        self.missed_warning_shown = False

        self.load_habits()
        missed = self.reset_if_new_day()
        self.create_widgets()
        self.refresh_list()

        if missed:
            self.show_missed_day_warning(missed)

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Daily Habit Tracker",
            font=("Arial", 22, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=12)

        self.date_label = tk.Label(
            self.root,
            text=f"Today: {date.today().isoformat()}",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )
        self.date_label.pack()

        # Progress section
        progress_frame = tk.Frame(self.root, bg=BG_COLOR)
        progress_frame.pack(fill="x", padx=25, pady=10)

        self.progress_label = tk.Label(
            progress_frame,
            text="Today: 0 / 0",
            font=("Arial", 12, "bold"),
            bg=BG_COLOR,
            fg=SUCCESS_COLOR,
        )
        self.progress_label.pack(anchor="w")

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Green.Horizontal.TProgressbar",
            troughcolor=BUTTON_COLOR,
            background=SUCCESS_COLOR,
            thickness=16,
        )
        self.progress = ttk.Progressbar(
            progress_frame,
            style="Green.Horizontal.TProgressbar",
            mode="determinate",
            maximum=100,
        )
        self.progress.pack(fill="x", pady=6)

        self.warning_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11),
            bg=BG_COLOR,
            fg=WARNING_COLOR,
            wraplength=680,
            justify="left",
        )
        self.warning_label.pack(fill="x", padx=25)

        add_frame = tk.Frame(self.root, bg=BG_COLOR)
        add_frame.pack(fill="x", padx=25, pady=10)

        self.habit_entry = tk.Entry(
            add_frame,
            font=("Arial", 13),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
        )
        self.habit_entry.pack(side=tk.LEFT, fill="x", expand=True)
        self.habit_entry.bind("<Return>", lambda e: self.add_habit())

        tk.Button(
            add_frame,
            text="Add Habit",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="#1e1e2e",
            command=self.add_habit,
        ).pack(side=tk.LEFT, padx=8)

        self.list_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.list_frame.pack(fill="both", expand=True, padx=25, pady=8)

        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Save",
            font=("Arial", 11),
            bg=SUCCESS_COLOR,
            fg="#1e1e2e",
            width=12,
            command=self.save_habits,
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_frame,
            text="Reset Today",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            width=12,
            command=self.reset_today,
        ).pack(side=tk.LEFT, padx=6)

        self.status = tk.Label(
            self.root,
            text="Add a habit to get started",
            bg=BG_COLOR,
            fg="#6c7086",
            font=("Arial", 10),
        )
        self.status.pack(pady=8)

    def add_habit(self):
        name = self.habit_entry.get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Please type a habit first.")
            return

        for habit in self.habits:
            if habit["name"].lower() == name.lower():
                messagebox.showinfo(
                    "Already Exists", "That habit is already in your list."
                )
                return

        self.habits.append(
            {
                "name": name,
                "done_today": False,
                "streak": 0,
                "best_streak": 0,
                "last_completed": "",
            }
        )
        self.habit_entry.delete(0, tk.END)
        self.save_habits()
        self.refresh_list()
        self.status.config(text=f"Added: {name}")

    def toggle_habit(self, index):
        habit = self.habits[index]
        today = date.today().isoformat()

        if habit["done_today"]:
            habit["done_today"] = False
            if habit["streak"] > 0:
                habit["streak"] -= 1
            if habit["last_completed"] == today:
                habit["last_completed"] = ""
        else:
            habit["done_today"] = True
            habit["streak"] += 1
            habit["last_completed"] = today
            if habit["streak"] > habit["best_streak"]:
                habit["best_streak"] = habit["streak"]

        self.save_habits()
        self.refresh_list()

    def delete_habit(self, index):
        name = self.habits[index]["name"]
        if not messagebox.askyesno("Delete Habit", f"Delete '{name}'?"):
            return
        self.habits.pop(index)
        self.save_habits()
        self.refresh_list()
        self.status.config(text=f"Deleted: {name}")

    def reset_today(self):
        if not messagebox.askyesno(
            "Reset Today", "Mark all habits as not done for today?"
        ):
            return
        today = date.today().isoformat()
        for habit in self.habits:
            if habit["done_today"]:
                habit["done_today"] = False
                if habit["streak"] > 0:
                    habit["streak"] -= 1
                if habit["last_completed"] == today:
                    habit["last_completed"] = ""
        self.save_habits()
        self.refresh_list()
        self.status.config(text="Today's checks were reset")

    def days_since(self, completed_date):
        if not completed_date:
            return None
        try:
            last = datetime.strptime(completed_date, "%Y-%m-%d").date()
            return (date.today() - last).days
        except ValueError:
            return None

    def reset_if_new_day(self):
        """Clear yesterday's checks and collect habits that missed a day."""
        missed = []
        today = date.today().isoformat()

        for habit in self.habits:
            days = self.days_since(habit["last_completed"])

            if habit["done_today"] and habit["last_completed"] != today:
                if days is None or days > 1:
                    if habit["streak"] > 0:
                        missed.append((habit["name"], habit["streak"]))
                    habit["streak"] = 0
                habit["done_today"] = False

            elif (
                not habit["done_today"]
                and days is not None
                and days > 1
                and habit["streak"] > 0
            ):
                missed.append((habit["name"], habit["streak"]))
                habit["streak"] = 0

        return missed

    def show_missed_day_warning(self, missed):
        names = ", ".join(name for name, streak in missed)
        text = (
            f"Missed day warning: these habits lost their streak: {names}. "
            "Check them off today to start a new streak."
        )
        self.warning_label.config(text=text)
        messagebox.showwarning(
            "Missed Day",
            f"You missed a day on:\n\n{names}\n\nThose streaks were reset to 0.",
        )

    def update_progress(self):
        total = len(self.habits)
        done = sum(1 for h in self.habits if h["done_today"])
        percent = 0 if total == 0 else int((done / total) * 100)

        self.progress["value"] = percent
        self.progress_label.config(text=f"Today: {done} / {total}  ({percent}%)")

        if total == 0:
            self.status.config(text="Add a habit to get started")
        elif done == total:
            self.status.config(text="All habits complete for today")
        else:
            self.status.config(text=f"{total - done} habit(s) left today")

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.update_progress()

        if not self.habits:
            empty = tk.Label(
                self.list_frame,
                text="No habits yet.\nTry adding: Drink water, Read 10 pages, Walk 20 minutes",
                font=("Arial", 12),
                bg=BG_COLOR,
                fg="#6c7086",
                justify="center",
            )
            empty.pack(pady=40)
            return

        for index, habit in enumerate(self.habits):
            card = tk.Frame(self.list_frame, bg=CARD_BG, padx=10, pady=8)
            card.pack(fill="x", pady=5)

            var = tk.BooleanVar(value=habit["done_today"])
            check = tk.Checkbutton(
                card,
                variable=var,
                bg=CARD_BG,
                activebackground=CARD_BG,
                command=lambda i=index: self.toggle_habit(i),
            )
            check.pack(side=tk.LEFT)

            days = self.days_since(habit["last_completed"])
            extra = ""
            color = SUCCESS_COLOR if habit["done_today"] else TEXT_COLOR
            if not habit["done_today"] and days is not None and days > 1:
                extra = "    MISSED"
                color = WARNING_COLOR

            info = tk.Label(
                card,
                text=f"{habit['name']}    Streak: {habit['streak']}    Best: {habit['best_streak']}{extra}",
                font=("Arial", 12),
                bg=CARD_BG,
                fg=color,
                anchor="w",
            )
            info.pack(side=tk.LEFT, fill="x", expand=True, padx=8)

            tk.Button(
                card,
                text="Delete",
                font=("Arial", 9),
                bg=DANGER_COLOR,
                fg="white",
                command=lambda i=index: self.delete_habit(i),
            ).pack(side=tk.RIGHT)

    def save_habits(self):
        data = {
            "saved_on": date.today().isoformat(),
            "habits": self.habits,
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_habits(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.habits = data.get("habits", [])
        except Exception:
            self.habits = []

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = HabitTracker()
    app.run()
