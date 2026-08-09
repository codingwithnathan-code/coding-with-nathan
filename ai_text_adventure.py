import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import ollama
import json
import os
from datetime import datetime

# ==================== COLORS ====================
BG_COLOR = "#1e1e2e"
TITLE_COLOR = "#cdd6f4"
TEXT_COLOR = "#cdd6f4"
ACCENT_COLOR = "#89b4fa"
SUCCESS_COLOR = "#a6e3a1"
BUTTON_COLOR = "#313244"
ENTRY_BG = "#313244"

SAVE_FILE = "adventure_save.json"

# pip install ollama
# ollama run llama3.1


class AITextAdventure:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Text Adventure - Coding With Nathan")
        self.root.geometry("1000x750")
        self.root.configure(bg=BG_COLOR)

        # Game state
        self.story_history = []
        self.inventory = []
        self.location = "Unknown Forest"
        self.player_name = "Adventurer"
        self.game_started = False

        self.create_widgets()
        self.show_welcome()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🌲 AI Text Adventure",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=15)

        # Story display area
        self.story_display = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 12),
            bg="#181825",
            fg=TEXT_COLOR,
            wrap=tk.WORD,
            height=22,
            state="disabled",
        )
        self.story_display.pack(padx=30, pady=10, fill="both", expand=True)

        # Input frame
        input_frame = tk.Frame(self.root, bg=BG_COLOR)
        input_frame.pack(pady=10, padx=30, fill="x")

        tk.Label(
            input_frame,
            text="Your Action:",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=("Arial", 11),
        ).pack(side=tk.LEFT)

        self.action_entry = tk.Entry(
            input_frame,
            font=("Arial", 13),
            bg=ENTRY_BG,
            fg=TEXT_COLOR,
            insertbackground="white",
            width=60,
        )
        self.action_entry.pack(side=tk.LEFT, padx=10, fill="x", expand=True)
        self.action_entry.bind("<Return>", lambda e: self.send_action())

        send_btn = tk.Button(
            input_frame,
            text="Go",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="#1e1e2e",
            command=self.send_action,
        )
        send_btn.pack(side=tk.LEFT, padx=5)

        # Bottom buttons
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="New Game",
            font=("Arial", 11),
            bg=SUCCESS_COLOR,
            fg="#1e1e2e",
            command=self.new_game,
        ).pack(side=tk.LEFT, padx=8)

        tk.Button(
            btn_frame,
            text="Save Game",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.save_game,
        ).pack(side=tk.LEFT, padx=8)

        tk.Button(
            btn_frame,
            text="Load Game",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.load_game,
        ).pack(side=tk.LEFT, padx=8)

        tk.Button(
            btn_frame,
            text="Show Inventory",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.show_inventory,
        ).pack(side=tk.LEFT, padx=8)

        # Status bar
        self.status_label = tk.Label(
            self.root, text="Ready", bg=BG_COLOR, fg="#6c7086", font=("Arial", 10)
        )
        self.status_label.pack(pady=5)

    def append_story(self, text, speaker="Narrator"):
        self.story_display.config(state="normal")
        if speaker == "Player":
            self.story_display.insert(tk.END, f"\n> {text}\n", "player")
        else:
            self.story_display.insert(tk.END, f"\n{text}\n", "narrator")
        self.story_display.tag_config("player", foreground="#89b4fa")
        self.story_display.tag_config("narrator", foreground="#cdd6f4")
        self.story_display.see(tk.END)
        self.story_display.config(state="disabled")

    def show_welcome(self):
        welcome = """
Welcome to the AI Text Adventure!

In this game, you explore a mysterious world by typing what you want to do.
A local Llama AI acts as the narrator and creates the story in real time.

Commands examples:
• look around
• go north
• talk to the stranger
• pick up the key
• check inventory

Click "New Game" to begin your adventure!
"""
        self.append_story(welcome)

    def new_game(self):
        name = simpledialog.askstring(
            "Character Name", "What is your name, adventurer?"
        )
        if not name:
            name = "Adventurer"

        self.player_name = name
        self.inventory = []
        self.location = "Dark Forest Clearing"
        self.story_history = []
        self.game_started = True

        self.story_display.config(state="normal")
        self.story_display.delete(1.0, tk.END)
        self.story_display.config(state="disabled")

        opening = f"""You wake up in a dark forest clearing. The air is cool and misty.
Tall ancient trees surround you. A narrow path leads north into the woods,
and you can hear the sound of running water somewhere to the east.

Your name is {self.player_name}. What do you do?"""

        self.append_story(opening)
        self.story_history.append({"role": "assistant", "content": opening})
        self.status_label.config(
            text=f"Playing as {self.player_name} | Location: {self.location}"
        )

    def send_action(self):
        if not self.game_started:
            messagebox.showinfo("Start Game", "Please start a New Game first.")
            return

        action = self.action_entry.get().strip()
        if not action:
            return

        self.action_entry.delete(0, tk.END)
        self.append_story(action, speaker="Player")
        self.status_label.config(text="Thinking...")

        # Build conversation history for the AI
        system_prompt = f"""You are the narrator of a text adventure game.
The player's name is {self.player_name}.
Current location: {self.location}
Inventory: {', '.join(self.inventory) if self.inventory else 'empty'}

Rules:
- Respond in 2-4 short paragraphs.
- Keep the story immersive and descriptive.
- React to the player's action naturally.
- Occasionally introduce items the player can pick up.
- If the player finds an item, clearly say they can take it.
- Keep the tone mysterious and adventurous.
- Do not break character.
- Never mention that you are an AI."""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.story_history[-8:])  # Keep last few exchanges
        messages.append({"role": "user", "content": action})

        try:
            response = ollama.chat(
                model="llama3.1",
                messages=messages,
            )
            reply = response["message"]["content"].strip()

            self.append_story(reply)
            self.story_history.append({"role": "user", "content": action})
            self.story_history.append({"role": "assistant", "content": reply})

            # Simple inventory detection
            lower_reply = reply.lower()
            if (
                "you pick up" in lower_reply
                or "you take" in lower_reply
                or "you found" in lower_reply
            ):
                # Very basic detection – can be improved
                pass

            self.status_label.config(
                text=f"Playing as {self.player_name} | Location: {self.location}"
            )

        except Exception as e:
            messagebox.showerror(
                "Ollama Error",
                f"Could not reach local Llama.\n\nMake sure Ollama is running and the model is installed:\n\nollama run llama3.1\n\nError: {e}",
            )
            self.status_label.config(text="Error – check Ollama")

    def show_inventory(self):
        if not self.inventory:
            messagebox.showinfo("Inventory", "Your inventory is empty.")
        else:
            items = "\n".join(f"• {item}" for item in self.inventory)
            messagebox.showinfo("Inventory", f"You are carrying:\n\n{items}")

    def save_game(self):
        if not self.game_started:
            messagebox.showinfo("Save", "No game in progress to save.")
            return

        data = {
            "player_name": self.player_name,
            "location": self.location,
            "inventory": self.inventory,
            "story_history": self.story_history,
            "saved_at": datetime.now().isoformat(),
        }

        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", f"Game saved successfully!\n({SAVE_FILE})")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            messagebox.showinfo("Load", "No saved game found.")
            return

        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.player_name = data.get("player_name", "Adventurer")
            self.location = data.get("location", "Unknown")
            self.inventory = data.get("inventory", [])
            self.story_history = data.get("story_history", [])
            self.game_started = True

            self.story_display.config(state="normal")
            self.story_display.delete(1.0, tk.END)
            self.story_display.config(state="disabled")

            # Replay the last part of the story
            for msg in self.story_history[-6:]:
                if msg["role"] == "user":
                    self.append_story(msg["content"], speaker="Player")
                else:
                    self.append_story(msg["content"])

            self.status_label.config(
                text=f"Loaded game – Playing as {self.player_name} | Location: {self.location}"
            )
            messagebox.showinfo("Loaded", "Game loaded successfully!")

        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AITextAdventure()
    app.run()
