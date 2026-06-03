import tkinter as tk
from tkinter import messagebox
import random

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
SUCCESS_COLOR = "#2ECC71"  # Green
TEXT_COLOR = "#ECF0F1"


class MadLibsGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mad Libs Story Generator - Coding With Nathan")
        self.root.geometry("800x800")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="Mad Libs Story Generator",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=20)

        # Instructions
        tk.Label(
            self.root,
            text="Fill in the words below and click Generate Story!",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        ).pack(pady=5)

        # Input Fields Frame
        input_frame = tk.Frame(self.root, bg=BG_COLOR)
        input_frame.pack(pady=10, padx=40, fill="x")

        # Create input fields
        self.entries = {}

        fields = [
            ("Your Name", "name"),
            ("Adjective (e.g. crazy, shiny)", "adj1"),
            ("Noun (e.g. elephant, spaceship)", "noun1"),
            ("Verb (e.g. run, jump)", "verb1"),
            ("Adjective (e.g. beautiful, scary)", "adj2"),
            ("Plural Noun (e.g. cats, robots)", "noun2"),
            ("Number", "number"),
            ("Famous Person", "person"),
            ("Verb Ending in -ing (e.g. dancing)", "verb2"),
            ("Place (e.g. beach, mountain)", "place"),
        ]

        for i, (label_text, key) in enumerate(fields):
            frame = tk.Frame(input_frame, bg=BG_COLOR)
            frame.pack(fill="x", pady=6)

            tk.Label(
                frame,
                text=label_text + ":",
                font=("Arial", 11),
                bg=BG_COLOR,
                fg=LABEL_COLOR,
                width=25,
                anchor="w",
            ).pack(side=tk.LEFT)

            entry = tk.Entry(frame, font=("Arial", 12), width=30)
            entry.pack(side=tk.LEFT, padx=10)
            self.entries[key] = entry

        # Buttons
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        generate_btn = tk.Button(
            btn_frame,
            text="Generate Story",
            font=("Arial", 14, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            width=18,
            height=2,
            command=self.generate_story,
        )
        generate_btn.pack(side=tk.LEFT, padx=15)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear All",
            font=("Arial", 12, "bold"),
            bg="#95A5A6",
            fg="white",
            width=12,
            command=self.clear_fields,
        )
        clear_btn.pack(side=tk.LEFT, padx=15)

        # Story Display
        tk.Label(
            self.root,
            text="Your Story:",
            font=("Arial", 14, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        ).pack(pady=10)

        self.story_text = tk.Text(
            self.root,
            font=("Arial", 12),
            height=15,
            wrap="word",
            bg="#34495E",
            fg=TEXT_COLOR,
        )
        self.story_text.pack(pady=10, padx=40, fill="both", expand=True)

    def generate_story(self):
        # Get all inputs
        words = {key: entry.get().strip() for key, entry in self.entries.items()}

        # Check if any field is empty
        if any(value == "" for value in words.values()):
            messagebox.showwarning("Missing Words", "Please fill in all the fields!")
            return

        # Story templates (randomly choose one)
        stories = [
            f"""
One sunny day, {words['name']} went to the {words['place']}.
They saw a {words['adj1']} {words['noun1']} sitting there.
Suddenly, the {words['noun1']} started to {words['verb1']} very fast!

{words['name']} was so {words['adj2']} that they dropped their {words['noun2']}.
Then {words['person']} appeared and said, "Let's {words['verb2']} together!"
They had a great time and counted {words['number']} stars that night.
            """,
            f"""
{words['name']} was walking through a {words['adj1']} forest when they found a magical {words['noun1']}.
As soon as they touched it, the {words['noun1']} began to {words['verb1']}.
{words['person']} appeared and shouted, "You must {words['verb2']} immediately!"

{words['name']} felt very {words['adj2']} and ran with {words['number']} {words['noun2']} following behind.
It was the most exciting day at the {words['place']} ever!
            """,
        ]

        # Choose random story and display it
        story = random.choice(stories)
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, story.strip())

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.story_text.delete(1.0, tk.END)

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = MadLibsGenerator()
    app.run()
