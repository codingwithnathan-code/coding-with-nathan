import tkinter as tk
from tkinter import messagebox
import random
import string

# ======= COLORS ========
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
SUCCESS_COLOR = "#2ECC71"  # Green
WARNING_COLOR = "#E74C3C"  # Red
TEXT_COLOR = "#ECF0F1"


class PasswordGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Generator - Coding With Nathan")
        self.root.geometry("620x520")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="Password Generator",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=20)

        # Length Frame
        length_frame = tk.Frame(self.root, bg=BG_COLOR)
        length_frame.pack(pady=10)

        tk.Label(
            length_frame,
            text="Password Lenth:",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        ).pack(side=tk.LEFT, padx=10)
        self.length_var = tk.IntVar(value=16)
        self.length_entry = tk.Entry(
            length_frame,
            textvariable=self.length_var,
            font=("Arial", 14),
            width=5,
            justify="center",
        )
        self.length_entry.pack(side=tk.LEFT)

        # Options Frame
        options_frame = tk.Frame(self.root, bg=BG_COLOR)
        options_frame.pack(pady=20)

        # Checkboxes
        self.uppercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        tk.Checkbutton(
            options_frame,
            text="Include Uppercase Letters (A-Z)",
            variable=self.uppercase_var,
            bg=BG_COLOR,
            fg=LABEL_COLOR,
            selectcolor=ACCENT_COLOR,
            font=("Arial", 11),
        ).pack(anchor="w", padx=50, pady=5)

        tk.Checkbutton(
            options_frame,
            text="Include Numbers (0-9)",
            variable=self.numbers_var,
            bg=BG_COLOR,
            fg=LABEL_COLOR,
            selectcolor=ACCENT_COLOR,
            font=("Arial", 11),
        ).pack(anchor="w", padx=50, pady=5)

        tk.Checkbutton(
            options_frame,
            text="Include Special Sysmbols (!@#$ etc.)",
            variable=self.symbols_var,
            bg=BG_COLOR,
            fg=LABEL_COLOR,
            selectcolor=ACCENT_COLOR,
            font=("Arial", 11),
        ).pack(anchor="w", padx=50, pady=5)

        # Generate Button
        generate_btn = tk.Button(
            self.root,
            text="Generate Password",
            font=("Arial", 14, "bold"),
            bg=BG_COLOR,
            fg="white",
            width=20,
            height=2,
            command=self.generate_password,
        )
        generate_btn.pack(pady=20)

        # Password Display
        tk.Label(
            self.root,
            text="Your Password:",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        ).pack(pady=5)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            self.root,
            textvariable=self.password_var,
            font=("Arial", 16),
            justify="center",
            width=40,
            state="readonly",
            readonlybackground=BG_COLOR,
            fg=SUCCESS_COLOR,
        )
        self.password_entry.pack(pady=10)

        # Copy Button
        copy_btn = tk.Button(
            self.root,
            text="Copy to Clipboard",
            font=("Arial", 12, "bold"),
            bg=SUCCESS_COLOR,
            fg=TITLE_COLOR,
            width=18,
            height=1,
            command=self.copy_to_clipboard,
        )
        copy_btn.pack(pady=10)

        # Status
        self.status_label = tk.Label(
            self.root,
            text="Ready to generate strong passwords!",
            font=("Arial", 10),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        )
        self.status_label.pack(pady=15)

    def generate_password(self):
        try:
            length = self.length_var.get()

            if length < 8 or length > 32:
                messagebox.showwarning(
                    "Invalid Length",
                    "Password length must be between 8 and 32 characters!",
                )
                return

            # Build character ppol
            characters = string.ascii_lowercase
            if self.uppercase_var.get():
                characters += string.ascii_uppercase
            if self.numbers_var.get():
                characters += string.digits
            if self.symbols_var.get():
                characters += string.punctuation

            # Generate password
            password = "".join(random.choice(characters) for _ in range(length))

            # Display password
            self.password_var.set(password)
            self.status_label.config(
                text=f"Generated {length}-character password!", fg=SUCCESS_COLOR
            )

        except Exception:
            messagebox.showerror("Error", "Something went wrong.  Please try again.")

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            self.status_label.config(
                text="Password copied to clipboard!", fg=SUCCESS_COLOR
            )
        else:
            messagebox.showwarning("No Password", "Generate a password first!")

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = PasswordGenerator()
    app.run()
