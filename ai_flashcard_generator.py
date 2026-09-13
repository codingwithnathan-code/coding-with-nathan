import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import ollama
import json
import os
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
CARD_BG = "#181825"

SAVE_FILE = "flashcards.json"


class AIFlashcardGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Study Flashcard Generator - Coding With Nathan")
        self.root.geometry("1000x760")
        self.root.configure(bg=BG_COLOR)

        self.cards = []
        self.current_index = 0
        self.showing_answer = False
        self.correct = 0
        self.wrong = 0
        self.topic = ""
        self.review_started = False

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="AI Study Flashcard Generator",
            font=("Arial", 22, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=12)

        # Topic input
        input_frame = tk.Frame(self.root, bg=BG_COLOR)
        input_frame.pack(fill="x", padx=25)

        tk.Label(input_frame, text="Topic:", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            side=tk.LEFT
        )
        self.topic_entry = tk.Entry(
            input_frame,
            font=("Arial", 13),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
        )
        self.topic_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=8)

        tk.Label(input_frame, text="# Cards:", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            side=tk.LEFT
        )
        self.count_var = tk.StringVar(value="8")
        tk.OptionMenu(input_frame, self.count_var, "5", "8", "10", "12").pack(
            side=tk.LEFT, padx=6
        )

        tk.Button(
            input_frame,
            text="Generate Cards",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="#1e1e2e",
            command=self.generate_cards,
        ).pack(side=tk.LEFT, padx=8)

        # Card display
        self.card_box = scrolledtext.ScrolledText(
            self.root,
            font=("Arial", 14),
            bg=CARD_BG,
            fg=TEXT_COLOR,
            wrap=tk.WORD,
            height=16,
            state="disabled",
        )
        self.card_box.pack(fill="both", expand=True, padx=25, pady=12)

        # Review buttons
        review_frame = tk.Frame(self.root, bg=BG_COLOR)
        review_frame.pack(pady=6)

        tk.Button(
            review_frame,
            text="Show Answer",
            font=("Arial", 11, "bold"),
            bg=WARNING_COLOR,
            fg="#1e1e2e",
            width=14,
            command=self.show_answer,
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            review_frame,
            text="I Got It",
            font=("Arial", 11, "bold"),
            bg=SUCCESS_COLOR,
            fg="#1e1e2e",
            width=12,
            command=self.mark_correct,
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            review_frame,
            text="Missed It",
            font=("Arial", 11, "bold"),
            bg=DANGER_COLOR,
            fg="white",
            width=12,
            command=self.mark_wrong,
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            review_frame,
            text="Next Card",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            width=12,
            command=self.next_card,
        ).pack(side=tk.LEFT, padx=6)

        # Bottom buttons
        bottom = tk.Frame(self.root, bg=BG_COLOR)
        bottom.pack(pady=10)

        tk.Button(
            bottom,
            text="Shuffle",
            font=("Arial", 10),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.shuffle_cards,
        ).pack(side=tk.LEFT, padx=6)
        tk.Button(
            bottom,
            text="Save Deck",
            font=("Arial", 10),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.save_deck,
        ).pack(side=tk.LEFT, padx=6)
        tk.Button(
            bottom,
            text="Load Deck",
            font=("Arial", 10),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.load_deck,
        ).pack(side=tk.LEFT, padx=6)
        tk.Button(
            bottom,
            text="Reset Score",
            font=("Arial", 10),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.reset_score,
        ).pack(side=tk.LEFT, padx=6)

        self.status = tk.Label(
            self.root,
            text="Enter a topic and click Generate Cards",
            bg=BG_COLOR,
            fg="#6c7086",
            font=("Arial", 10),
        )
        self.status.pack(pady=6)

        self.show_welcome()

    def set_card_text(self, text):
        self.card_box.config(state="normal")
        self.card_box.delete("1.0", tk.END)
        self.card_box.insert("1.0", text)
        self.card_box.config(state="disabled")

    def show_welcome(self):
        self.set_card_text(
            "Welcome to the AI Study Flashcard Generator!\n\n"
            "1. Type a topic, such as Python lists or World War 2.\n"
            "2. Click Generate Cards.\n"
            "3. Read the question, try to answer it in your head, then click Show Answer.\n"
            "4. Mark I Got It or Missed It to keep score.\n\n"
            "Make sure Ollama is running:\nollama run llama3.1"
        )

    def generate_cards(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Missing Topic", "Please enter a topic first.")
            return

        count = int(self.count_var.get())
        self.topic = topic
        self.status.config(text="Creating flashcards with local Llama...")
        self.set_card_text("Generating cards...\nThis may take 10-30 seconds.")
        self.root.update()

        prompt = f"""Create {count} study flashcards about: {topic}

Use this exact format for every card:

Q: [short question]
A: [short clear answer]

Rules:
- Make beginner-friendly questions.
- Keep answers short.
- Do not add extra commentary.
- Do not number the cards.
- Create exactly {count} cards.
"""

        try:
            response = ollama.chat(
                model="gemma4:26b",
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response["message"]["content"]
            cards = self.parse_cards(raw)

            if not cards:
                cards = self.fallback_cards(topic)

            self.cards = cards
            self.current_index = 0
            self.showing_answer = False
            self.correct = 0
            self.wrong = 0
            self.review_started = True
            self.show_question()
            self.status.config(text=f"Created {len(self.cards)} cards about {topic}")

        except Exception as e:
            messagebox.showerror(
                "Ollama Error",
                "Could not reach local Llama.\n\n"
                "Make sure Ollama is running:\n"
                "ollama run llama3.1\n\n"
                f"Error: {e}",
            )
            self.cards = self.fallback_cards(topic)
            self.current_index = 0
            self.review_started = True
            self.show_question()
            self.status.config(text="Used fallback cards because Ollama failed")

    def parse_cards(self, text):
        cards = []
        question = None

        for line in text.splitlines():
            line = line.strip()
            if line.lower().startswith("q:"):
                question = line[2:].strip()
            elif line.lower().startswith("a:") and question:
                answer = line[2:].strip()
                if question and answer:
                    cards.append({"question": question, "answer": answer})
                question = None

        return cards

    def fallback_cards(self, topic):
        return [
            {
                "question": f"What is one basic fact about {topic}?",
                "answer": f"{topic} is a study topic. Replace this card after Llama is working.",
            },
            {
                "question": f"Why might someone study {topic}?",
                "answer": "To learn the main ideas and practice recalling them from memory.",
            },
            {
                "question": "What is the point of a flashcard?",
                "answer": "To test yourself. Look at the question, try to answer, then check.",
            },
        ]

    def current_card(self):
        if not self.cards:
            return None
        return self.cards[self.current_index]

    def show_question(self):
        card = self.current_card()
        if not card:
            self.set_card_text("No cards yet.")
            return

        self.showing_answer = False
        total = len(self.cards)
        self.set_card_text(
            f"Topic: {self.topic}\n"
            f"Card {self.current_index + 1} of {total}\n"
            f"Score: {self.correct} correct, {self.wrong} missed\n\n"
            f"QUESTION:\n{card['question']}\n\n"
            "Try to answer in your head, then click Show Answer."
        )

    def show_answer(self):
        if not self.review_started:
            return
        card = self.current_card()
        if not card:
            return

        self.showing_answer = True
        total = len(self.cards)
        self.set_card_text(
            f"Topic: {self.topic}\n"
            f"Card {self.current_index + 1} of {total}\n"
            f"Score: {self.correct} correct, {self.wrong} missed\n\n"
            f"QUESTION:\n{card['question']}\n\n"
            f"ANSWER:\n{card['answer']}"
        )

    def mark_correct(self):
        if not self.review_started:
            return
        if not self.showing_answer:
            messagebox.showinfo(
                "Show Answer First", "Click Show Answer before scoring the card."
            )
            return
        self.correct += 1
        self.next_card()

    def mark_wrong(self):
        if not self.review_started:
            return
        if not self.showing_answer:
            messagebox.showinfo(
                "Show Answer First", "Click Show Answer before scoring the card."
            )
            return
        self.wrong += 1
        self.next_card()

    def next_card(self):
        if not self.cards:
            return

        self.current_index += 1
        if self.current_index >= len(self.cards):
            self.show_summary()
            self.current_index = 0

        self.show_question()

    def show_summary(self):
        total = self.correct + self.wrong
        percent = 0 if total == 0 else round((self.correct / total) * 100)
        messagebox.showinfo(
            "Deck Complete",
            f"You finished the deck!\n\n"
            f"Correct: {self.correct}\n"
            f"Missed: {self.wrong}\n"
            f"Score: {percent}%\n\n"
            "The deck will start over so you can review again.",
        )

    def shuffle_cards(self):
        if not self.cards:
            return
        random.shuffle(self.cards)
        self.current_index = 0
        self.showing_answer = False
        self.show_question()
        self.status.config(text="Deck shuffled")

    def reset_score(self):
        self.correct = 0
        self.wrong = 0
        self.current_index = 0
        self.showing_answer = False
        if self.cards:
            self.show_question()
        self.status.config(text="Score reset")

    def save_deck(self):
        if not self.cards:
            messagebox.showinfo("Save", "No cards to save.")
            return

        data = {
            "topic": self.topic,
            "cards": self.cards,
            "saved_at": datetime.now().isoformat(),
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        messagebox.showinfo("Saved", f"Deck saved to {SAVE_FILE}")

    def load_deck(self):
        if not os.path.exists(SAVE_FILE):
            messagebox.showinfo("Load", "No saved deck found.")
            return

        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.topic = data.get("topic", "Saved Deck")
        self.cards = data.get("cards", [])
        self.current_index = 0
        self.correct = 0
        self.wrong = 0
        self.review_started = True
        self.topic_entry.delete(0, tk.END)
        self.topic_entry.insert(0, self.topic)
        self.show_question()
        self.status.config(text=f"Loaded {len(self.cards)} cards")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIFlashcardGenerator()
    app.run()
