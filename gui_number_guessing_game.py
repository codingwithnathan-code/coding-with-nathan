import tkinter as tk
from tkinter import messagebox
import random


class GuessingGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Number Guessing Gmae - Coding With Nathan")
        self.root.geometry("520x480")
        self.root.configure(bg="#2C3E50")
        self.root.resizable(False, False)

        # Game variables
        self.secret_number = random.randint(1, 100)
        self.guesses = 0

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🎲 Number Guessing Game 🎲",
            font=("Arial", 24, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1",
        )
        title.pack(pady=20)

        # Insturction
        instruction = tk.Label(
            self.root,
            text="I'm thinking of a number between 1 and 100",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#BDC3C7",
        )
        instruction.pack(pady=5)

        # Entry box
        self.guess_entry = tk.Entry(
            self.root, font=("Arial", 18), justify="center", width=15
        )
        self.guess_entry.pack(pady=15)
        self.guess_entry.focus()  # Auto-focus on entry

        # Feedback Label
        self.feedback = tk.Label(
            self.root, text="", font=("Arial", 14, "bold"), bg="#2C3E50", fg="#F1C40F"
        )
        self.feedback.pack(pady=10)

        # Guess Button
        guess_btn = tk.Button(
            self.root,
            text="Make Guess",
            font=("Arial", 14, "bold"),
            bg="#3498DB",
            fg="white",
            width=15,
            height=2,
            command=self.make_guess,
        )
        guess_btn.pack(pady=10)

        # Play Again Button
        self.play_again_btn = tk.Button(
            self.root,
            text="Play Again",
            font=("Arial", 14, "bold"),
            bg="#3498DB",
            fg="white",
            width=12,
            command=self.reset_game,
        )
        self.play_again_btn.pack(pady=8)
        self.play_again_btn.config(state="disabled")  # Disabled at start

        # Status label
        self.status = tk.Label(
            self.root, text="Good luck!", font=("Arial", 10), bg="#2C3E50", fg="#95A5A6"
        )
        self.status.pack(pady=15)

    def make_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.guesses += 1
            if guess < 1 or guess > 100:
                messagebox.showwarning(
                    "Invalid Input", "Please enter a number between 1 and 100!"
                )
                self.guess_entry.delete(0, tk.END)
                return

            if guess == self.secret_number:
                messagebox.showinfo(
                    "Congratulations!",
                    f"You guessed the number {self.secret_number} correctly!\n"
                    f"It took you {self.guesses}!",
                )
                self.feedback.config(text=" You Win!", fg="#2ECC71")
                self.play_again_btn.config(state="normal")
                self.guess_entry.config(state="disabled")

            elif guess < self.secret_number:
                self.feedback.config(text="Too Low! Try higher.", fg="#E74C3C")
            else:
                self.feedback.config(text="Too High! Try lower.", fg="#E74C3C")

            self.guess_entry.delete(0, tk.END)  # Clear entry

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            self.guess_entry.delete(0, tk.END)

    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.guesses = 0
        self.feedback.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state="normal")
        self.play_again_btn.config(state="disabled")
        self.status.config(text="New game started! Good luck!")
        self.guess_entry.focus()

    def run(self):
        self.root.mainloop()


# Run the game
if __name__ == "__main__":
    game = GuessingGame()
    game.run()
