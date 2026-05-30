import tkinter as tk
from tkinter import messagebox
import random

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
CORRECT_COLOR = "#2ECC71"  # Green
WRONG_COLOR = "#E74C3C"  # Red
TEXT_COLOR = "#ECF0F1"


class QuizGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Game - Coding With Nathan")
        self.root.geometry("800x700")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Quiz data
        self.questions = self.get_questions()
        self.current_question = 0
        self.score = 0
        self.selected_answer = None

        self.create_widgets()
        self.load_question()

    def get_questions(self):
        return [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "answer": "Paris",
            },
            {
                "question": "Which programming language is this quiz written in?",
                "options": ["Java", "Python", "C++", "JavaScript"],
                "answer": "Python",
            },
            {
                "question": "What does CPU stand for?",
                "options": [
                    "Central Processing Unit",
                    "Computer Personal Unit",
                    "Central Power Unit",
                    "Control Processing Unit",
                ],
                "answer": "Central Processing Unit",
            },
            {
                "question": "How many continents are there on Earth?",
                "options": ["5", "6", "7", "8"],
                "answer": "7",
            },
            {
                "question": "What year did Python first appear?",
                "options": ["1989", "1991", "1995", "2000"],
                "answer": "1991",
            },
            {
                "question": "Which of these is not a programming language?",
                "options": ["Python", "Java", "HTML", "C++"],
                "answer": "HTML",
            },
            {
                "question": "What does GUI stand for?",
                "options": [
                    "General User Interface",
                    "Graphical User Interface",
                    "Global User Input",
                    "Graphic Universal Interface",
                ],
                "answer": "Graphical User Interface",
            },
        ]

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="Quiz Game",
            font=("Arial", 28, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=20)

        # Question counter
        self.question_counter = tk.Label(
            self.root, text="", font=("Arial", 12), bg=BG_COLOR, fg=LABEL_COLOR
        )
        self.question_counter.pack(pady=5)

        # Question text
        self.question_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 16),
            wraplength=700,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            justify="center",
        )
        self.question_label.pack(pady=30, padx=40)

        # Answer buttons frame
        self.buttons_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.buttons_frame.pack(pady=20)

        # Create 4 answer buttons
        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text="",
                font=("Arial", 12),
                width=50,
                height=2,
                bg=ACCENT_COLOR,
                fg="white",
                command=lambda x=i: self.select_answer(x),
            )
            btn.pack(pady=8)
            self.answer_buttons.append(btn)

        # Score display
        self.score_label = tk.Label(
            self.root,
            text="Score: 0",
            font=("Arial", 14, "bold"),
            bg=BG_COLOR,
            fg=ACCENT_COLOR,
        )
        self.score_label.pack(pady=20)

        # Next button (hidden until answer selected)
        self.next_button = tk.Button(
            self.root,
            text="Next Question",
            font=("Arial", 12, "bold"),
            bg="#F1C40F",
            fg="black",
            width=20,
            height=2,
            command=self.next_question,
        )
        self.next_button.pack(pady=10)
        self.next_button.pack_forget()  # Hide initially

    def load_question(self):
        if self.current_question >= len(self.questions):
            self.show_results()
            return

        question = self.questions[self.current_question]

        # Update question counter
        self.question_counter.config(
            text=f"Question {self.current_question + 1} of {len(self.questions)}"
        )

        # Update question text
        self.question_label.config(text=question["question"])

        # Shuffle options
        options = question["options"][:]
        random.shuffle(options)

        # Update buttons
        for i, btn in enumerate(self.answer_buttons):
            btn.config(text=options[i], state="normal", bg=ACCENT_COLOR)
            btn.option_text = options[i]  # Store the text for checking

        self.selected_answer = None
        self.next_button.pack_forget()

    def select_answer(self, index):
        if self.selected_answer is not None:
            return

        self.selected_answer = index
        question = self.questions[self.current_question]
        selected_text = self.answer_buttons[index].option_text

        # Disable all buttons
        for btn in self.answer_buttons:
            btn.config(state="disabled")

        # Highlight correct and wrong answers
        for btn in self.answer_buttons:
            if btn.option_text == question["answer"]:
                btn.config(bg=CORRECT_COLOR)
            elif btn.option_text == selected_text:
                btn.config(bg=WRONG_COLOR)

        # Update score if correct
        if selected_text == question["answer"]:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")

        self.next_button.pack(pady=10)

    def next_question(self):
        self.current_question += 1
        self.load_question()

    def show_results(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

        result_frame = tk.Frame(self.root, bg=BG_COLOR)
        result_frame.pack(expand=True)

        tk.Label(
            result_frame,
            text="Quiz Complete!",
            font=("Arial", 28, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        ).pack(pady=30)

        percentage = (self.score / len(self.questions)) * 100

        tk.Label(
            result_frame,
            text=f"Your Score: {self.score} / {len(self.questions)}",
            font=("Arial", 20),
            bg=BG_COLOR,
            fg=ACCENT_COLOR,
        ).pack(pady=10)

        tk.Label(
            result_frame,
            text=f"{percentage:.1f}%",
            font=("Arial", 48, "bold"),
            bg=BG_COLOR,
            fg=CORRECT_COLOR,
        ).pack(pady=10)

        if percentage >= 80:
            message = "Excellent Work!"
        elif percentage >= 60:
            message = "Good Job!"
        else:
            message = "Keep Practicing!"

        tk.Label(
            result_frame, text=message, font=("Arial", 18), bg=BG_COLOR, fg=TITLE_COLOR
        ).pack(pady=20)

        restart_btn = tk.Button(
            result_frame,
            text="Play Again",
            font=("Arial", 14, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            width=20,
            height=2,
            command=self.restart_quiz,
        )
        restart_btn.pack(pady=30)

    def restart_quiz(self):
        self.current_question = 0
        self.score = 0
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.load_question()

    def run(self):
        self.root.mainloop()


# Run the game
if __name__ == "__main__":
    game = QuizGame()
    game.run()
