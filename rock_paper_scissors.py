import tkinter as tk
from tkinter import messagebox
import random

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
WIN_COLOR = "#2ECC71"  # Green
LOSE_COLOR = "#E74C3C"  # Red
TIE_COLOR = "#F1C40F"  # Yellow
TEXT_COLOR = "#ECF0F1"


class RockPaperScissors:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors - Coding With Nathan")
        self.root.geometry("750x700")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Game statistics
        self.player_wins = 0
        self.computer_wins = 0
        self.ties = 0
        self.history = []  # Store last 10 rounds

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="Rock Paper Scissors",
            font=("Arial", 26, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=20)

        # Score Frame
        score_frame = tk.Frame(self.root, bg=BG_COLOR)
        score_frame.pack(pady=10)

        self.player_score_label = tk.Label(
            score_frame,
            text="You: 0",
            font=("Arial", 14, "bold"),
            bg=BG_COLOR,
            fg=WIN_COLOR,
        )
        self.player_score_label.pack(side=tk.LEFT, padx=30)

        self.computer_score_label = tk.Label(
            score_frame,
            text="Computer: 0",
            font=("Arial", 14, "bold"),
            bg=BG_COLOR,
            fg=LOSE_COLOR,
        )
        self.computer_score_label.pack(side=tk.LEFT, padx=30)

        self.tie_label = tk.Label(
            score_frame,
            text="Ties: 0",
            font=("Arial", 14, "bold"),
            bg=BG_COLOR,
            fg=TIE_COLOR,
        )
        self.tie_label.pack(side=tk.LEFT, padx=30)

        # Game Area
        game_frame = tk.Frame(self.root, bg=BG_COLOR)
        game_frame.pack(pady=20)

        # Instruction
        tk.Label(
            game_frame,
            text="Choose your move:",
            font=("Arial", 14),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        ).pack(pady=10)

        # Buttons Frame
        btn_frame = tk.Frame(game_frame, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        rock_btn = tk.Button(
            btn_frame,
            text="🪨 Rock",
            font=("Arial", 14, "bold"),
            width=12,
            height=3,
            bg="#555555",
            fg="white",
            command=lambda: self.play("Rock"),
        )
        rock_btn.grid(row=0, column=0, padx=10)

        paper_btn = tk.Button(
            btn_frame,
            text="📄 Paper",
            font=("Arial", 14, "bold"),
            width=12,
            height=3,
            bg="#3498DB",
            fg="white",
            command=lambda: self.play("Paper"),
        )
        paper_btn.grid(row=0, column=1, padx=10)

        scissors_btn = tk.Button(
            btn_frame,
            text="✂️ Scissors",
            font=("Arial", 14, "bold"),
            width=12,
            height=3,
            bg="#E67E22",
            fg="white",
            command=lambda: self.play("Scissors"),
        )
        scissors_btn.grid(row=0, column=2, padx=10)

        # Result Area
        self.result_label = tk.Label(
            self.root,
            text="Make your move!",
            font=("Arial", 16, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )
        self.result_label.pack(pady=20)

        # History
        history_frame = tk.Frame(self.root, bg=BG_COLOR)
        history_frame.pack(pady=10, fill="both", padx=40)

        tk.Label(
            history_frame,
            text="Game History (Last 10 Rounds)",
            font=("Arial", 12, "bold"),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        ).pack(anchor="w")

        self.history_listbox = tk.Listbox(
            history_frame, font=("Arial", 11), height=8, bg="#34495E", fg=TEXT_COLOR
        )
        self.history_listbox.pack(fill="both", expand=True, pady=5)

        # Reset Button
        reset_btn = tk.Button(
            self.root,
            text="Reset Statistics",
            font=("Arial", 12, "bold"),
            bg="#95A5A6",
            fg="white",
            width=20,
            command=self.reset_statistics,
        )
        reset_btn.pack(pady=15)

    def play(self, player_choice):
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)

        # Determine the winner
        if player_choice == computer_choice:
            result = "It's a Tie!"
            color = TIE_COLOR
            self.ties += 1
        elif (
            (player_choice == "Rock" and computer_choice == "Scissors")
            or (player_choice == "Paper" and computer_choice == "Rock")
            or (player_choice == "Scissors" and computer_choice == "Paper")
        ):
            result = "You Win!"
            color = WIN_COLOR
            self.player_wins += 1
        else:
            result = "Computer Wins!"
            color = LOSE_COLOR
            self.computer_wins += 1

        # Update results
        self.result_label.config(
            text=f"You: {player_choice} : Computer: {computer_choice}\n{result}",
            fg=color,
        )

        # Add to history
        history_text = f"You: {player_choice} : Computer: {computer_choice} = {result}"
        self.history.insert(0, history_text)
        if len(self.history) > 10:
            self.history.pop()

        self.update_history()
        self.update_scores()

    def update_scores(self):
        self.player_score_label.config(text=f"You: {self.player_wins}")
        self.computer_score_label.config(text=f"Computer: {self.computer_wins}")
        self.tie_label.config(text=f"Ties: {self.ties}")

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history:
            self.history_listbox.insert(tk.END, entry)

    def reset_statistics(self):
        if messagebox.askyesno(
            "Reset Statistics", "Are you sure you want to reset all scores?"
        ):
            self.player_wins = 0
            self.computer_wins = 0
            self.ties = 0
            self.history.clear()
            self.update_scores()
            self.update_history()
            self.result_label.config(text="Statistics have been reset!", fg=TEXT_COLOR)

    def run(self):
        self.root.mainloop()


# Run the game
if __name__ == "__main__":
    game = RockPaperScissors()
    game.run()
