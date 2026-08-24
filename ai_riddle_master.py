import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import ollama
import json
import os
import time
import random
from datetime import datetime

# ==================== COLORS ====================
BG_COLOR = "#1e1e2e"
TITLE_COLOR = "#cdd6f4"
TEXT_COLOR = "#cdd6f4"
ACCENT_COLOR = "#89b4fa"
SUCCESS_COLOR = "#a6e3a1"
WARNING_COLOR = "#f9e2af"
DANGER_COLOR = "#f38ba8"
BUTTON_COLOR = "#313244"
ENTRY_BG = "#313244"

SAVE_FILE = "escape_room_save.json"


class AIRiddleMaster:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Riddle Master – Escape Room - Coding With Nathan")
        self.root.geometry("1050x780")
        self.root.configure(bg=BG_COLOR)

        # Game state
        self.player_name = "Player"
        self.current_room = 1
        self.max_rooms = 5
        self.hints_used = 0
        self.score = 1000
        self.start_time = None
        self.current_riddle = ""
        self.current_answer = ""
        self.solved_rooms = []
        self.game_started = False
        self.waiting_for_answer = False

        self.create_widgets()
        self.show_welcome()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🔐 AI Riddle Master – Escape Room",
            font=("Arial", 22, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=12)

        # Main story area
        self.story_display = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 12),
            bg="#181825",
            fg=TEXT_COLOR,
            wrap=tk.WORD,
            height=24,
            state="disabled",
        )
        self.story_display.pack(padx=25, pady=8, fill="both", expand=True)

        # Input area
        input_frame = tk.Frame(self.root, bg=BG_COLOR)
        input_frame.pack(pady=8, padx=25, fill="x")

        self.action_entry = tk.Entry(
            input_frame,
            font=("Arial", 13),
            bg=ENTRY_BG,
            fg=TEXT_COLOR,
            insertbackground="white",
        )
        self.action_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))
        self.action_entry.bind("<Return>", lambda e: self.submit_answer())

        tk.Button(
            input_frame,
            text="Submit",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="#1e1e2e",
            command=self.submit_answer,
            width=10,
        ).pack(side=tk.LEFT)

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="New Game",
            font=("Arial", 11, "bold"),
            bg=SUCCESS_COLOR,
            fg="#1e1e2e",
            width=14,
            command=self.new_game,
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_frame,
            text="Get Hint",
            font=("Arial", 11),
            bg=WARNING_COLOR,
            fg="#1e1e2e",
            width=12,
            command=self.get_hint,
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_frame,
            text="Save",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            width=10,
            command=self.save_game,
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_frame,
            text="Load",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            width=10,
            command=self.load_game,
        ).pack(side=tk.LEFT, padx=6)

        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready • Click New Game to start",
            bg=BG_COLOR,
            fg="#6c7086",
            font=("Arial", 10),
        )
        self.status_label.pack(pady=6)

    def append_text(self, text, tag="normal"):
        self.story_display.config(state="normal")
        if tag == "player":
            self.story_display.insert(tk.END, f"\n> {text}\n", "player")
        elif tag == "system":
            self.story_display.insert(tk.END, f"\n{text}\n", "system")
        elif tag == "riddle":
            self.story_display.insert(tk.END, f"\n{text}\n", "riddle")
        else:
            self.story_display.insert(tk.END, f"\n{text}\n", "normal")

        self.story_display.tag_config("player", foreground="#89b4fa")
        self.story_display.tag_config("system", foreground="#a6e3a1")
        self.story_display.tag_config("riddle", foreground="#f9e2af")
        self.story_display.tag_config("normal", foreground="#cdd6f4")
        self.story_display.see(tk.END)
        self.story_display.config(state="disabled")

    def show_welcome(self):
        welcome = """Welcome to the AI Riddle Master Escape Room!

You are trapped inside a mysterious facility. To escape you must solve a series of riddles 
generated by a local Llama AI.

• There are 5 rooms to escape
• Each room has a unique riddle
• You can ask for hints (but they cost points)
• Your final score depends on time and hints used

Click "New Game" to begin your escape!"""
        self.append_text(welcome)

    def new_game(self):
        name = simpledialog.askstring("Player Name", "What is your name?")
        if not name:
            name = "Player"

        self.player_name = name
        self.current_room = 1
        self.hints_used = 0
        self.score = 1000
        self.start_time = time.time()
        self.solved_rooms = []
        self.game_started = True
        self.waiting_for_answer = False

        self.story_display.config(state="normal")
        self.story_display.delete(1.0, tk.END)
        self.story_display.config(state="disabled")

        intro = f"""Welcome, {self.player_name}.

The heavy door slams shut behind you. You are locked inside Room 1 of 5.
A glowing terminal flickers to life on the wall...

Generating your first riddle..."""
        self.append_text(intro, "system")
        self.status_label.config(
            text=f"Room {self.current_room}/{self.max_rooms} • Score: {self.score}"
        )

        self.root.after(800, self.generate_riddle)

    def generate_riddle(self):
        """Ask local Llama to create a riddle for the current room"""
        self.status_label.config(text="AI is creating a riddle...")

        difficulty = (
            "easy"
            if self.current_room <= 2
            else "medium" if self.current_room <= 4 else "hard"
        )

        prompt = f"""You are a Riddle Master creating an escape room.

Create one original {difficulty} riddle for Room {self.current_room} of an escape room.
Theme ideas: technology, ancient secrets, logic, nature, or mystery.

Respond in this exact format:

RIDDLE:
[the riddle text here]

ANSWER:
[the single correct answer in lowercase]

Keep the riddle clever but fair. The answer should be one or two words."""

        try:
            response = ollama.chat(
                model="llama3.1", messages=[{"role": "user", "content": prompt}]
            )
            content = response["message"]["content"].strip()

            # Parse the response
            if "RIDDLE:" in content and "ANSWER:" in content:
                riddle_part = content.split("ANSWER:")[0].replace("RIDDLE:", "").strip()
                answer_part = content.split("ANSWER:")[1].strip().lower()
                # Clean answer (take first line only)
                answer_part = answer_part.split("\n")[0].strip()

                self.current_riddle = riddle_part
                self.current_answer = answer_part
                self.waiting_for_answer = True

                self.append_text(f"─── ROOM {self.current_room} ───", "system")
                self.append_text(self.current_riddle, "riddle")
                self.append_text(
                    "Type your answer below and press Submit (or Enter).", "system"
                )
                self.status_label.config(
                    text=f"Room {self.current_room}/{self.max_rooms} • Hints used: {self.hints_used} • Score: {self.score}"
                )
            else:
                # Fallback riddle if parsing fails
                self.use_fallback_riddle()

        except Exception as e:
            messagebox.showerror(
                "Ollama Error",
                f"Could not reach local Llama.\n\nMake sure Ollama is running:\nollama run llama3.1\n\nError: {e}",
            )
            self.use_fallback_riddle()

    def use_fallback_riddle(self):
        """Simple fallback riddles in case the AI fails"""
        fallbacks = [
            (
                "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
                "echo",
            ),
            ("The more you take, the more you leave behind. What am I?", "footsteps"),
            ("What has keys but can't open locks?", "piano"),
            ("What can travel around the world while staying in a corner?", "stamp"),
            ("What has a head, a tail, is brown, and has no legs?", "penny"),
        ]
        riddle, answer = random.choice(fallbacks)
        self.current_riddle = riddle
        self.current_answer = answer
        self.waiting_for_answer = True

        self.append_text(f"─── ROOM {self.current_room} ───", "system")
        self.append_text(self.current_riddle, "riddle")
        self.append_text("Type your answer and press Submit.", "system")

    def submit_answer(self):
        if not self.game_started or not self.waiting_for_answer:
            return

        answer = self.action_entry.get().strip().lower()
        if not answer:
            return

        self.action_entry.delete(0, tk.END)
        self.append_text(answer, "player")

        # Check answer (flexible matching)
        correct = False
        if answer == self.current_answer:
            correct = True
        elif self.current_answer in answer or answer in self.current_answer:
            correct = True

        if correct:
            self.waiting_for_answer = False
            self.solved_rooms.append(self.current_room)
            self.score += 150

            self.append_text("✓ Correct! The door unlocks...", "system")

            if self.current_room >= self.max_rooms:
                self.escape_success()
            else:
                self.current_room += 1
                self.append_text(f"You move into Room {self.current_room}...", "system")
                self.root.after(1200, self.generate_riddle)
        else:
            self.score = max(0, self.score - 40)
            self.append_text(
                "✗ Incorrect. The terminal buzzes angrily. Try again.", "system"
            )
            self.status_label.config(
                text=f"Room {self.current_room}/{self.max_rooms} • Hints used: {self.hints_used} • Score: {self.score}"
            )

    def get_hint(self):
        if not self.game_started or not self.waiting_for_answer:
            messagebox.showinfo("Hint", "No active riddle to hint.")
            return

        self.hints_used += 1
        self.score = max(0, self.score - 80)

        prompt = f"""Give a helpful but not obvious hint for this riddle.
Do not reveal the answer directly.

Riddle: {self.current_riddle}
Answer: {self.current_answer}

Provide one short hint only."""

        try:
            response = ollama.chat(
                model="llama3.1", messages=[{"role": "user", "content": prompt}]
            )
            hint = response["message"]["content"].strip()
            self.append_text(f"💡 Hint: {hint}", "system")
        except:
            # Simple fallback hint
            if len(self.current_answer) > 0:
                hint = f"The answer starts with '{self.current_answer[0]}' and has {len(self.current_answer)} letters."
                self.append_text(f"💡 Hint: {hint}", "system")

        self.status_label.config(
            text=f"Room {self.current_room}/{self.max_rooms} • Hints used: {self.hints_used} • Score: {self.score}"
        )

    def escape_success(self):
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60

        # Time bonus
        time_bonus = max(0, 400 - elapsed)
        final_score = self.score + time_bonus

        result = f"""
🎉 CONGRATULATIONS {self.player_name.upper()}! 🎉

You escaped all {self.max_rooms} rooms!

Time taken: {minutes}m {seconds}s
Hints used: {self.hints_used}
Base score: {self.score}
Time bonus: +{time_bonus}

FINAL SCORE: {final_score}

You are free!
"""
        self.append_text(result, "system")
        self.game_started = False
        self.waiting_for_answer = False
        self.status_label.config(text=f"ESCAPED! Final Score: {final_score}")

    def save_game(self):
        if not self.game_started:
            messagebox.showinfo("Save", "No active game to save.")
            return

        data = {
            "player_name": self.player_name,
            "current_room": self.current_room,
            "hints_used": self.hints_used,
            "score": self.score,
            "start_time": self.start_time,
            "current_riddle": self.current_riddle,
            "current_answer": self.current_answer,
            "solved_rooms": self.solved_rooms,
            "waiting_for_answer": self.waiting_for_answer,
        }

        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", "Game saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            messagebox.showinfo("Load", "No saved game found.")
            return

        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.player_name = data["player_name"]
            self.current_room = data["current_room"]
            self.hints_used = data["hints_used"]
            self.score = data["score"]
            self.start_time = data["start_time"]
            self.current_riddle = data["current_riddle"]
            self.current_answer = data["current_answer"]
            self.solved_rooms = data["solved_rooms"]
            self.waiting_for_answer = data["waiting_for_answer"]
            self.game_started = True

            self.story_display.config(state="normal")
            self.story_display.delete(1.0, tk.END)
            self.story_display.config(state="disabled")

            self.append_text(
                f"Game loaded – Welcome back, {self.player_name}!", "system"
            )
            self.append_text(f"─── ROOM {self.current_room} ───", "system")
            self.append_text(self.current_riddle, "riddle")
            self.append_text("Type your answer and press Submit.", "system")

            self.status_label.config(
                text=f"Room {self.current_room}/{self.max_rooms} • Hints used: {self.hints_used} • Score: {self.score}"
            )
            messagebox.showinfo("Loaded", "Game loaded successfully!")

        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIRiddleMaster()
    app.run()
