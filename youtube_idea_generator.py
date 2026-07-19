import tkinter as tk
from tkinter import messagebox, scrolledtext
import ollama  # pip install ollama
import json
import os

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"
ACCENT_COLOR = "#3498DB"
TEXT_COLOR = "#ECF0F1"


class YouTubeIdeaGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Video Idea + Script Generator - Coding With Nathan")
        self.root.geometry("1000x800")
        self.root.configure(bg=BG_COLOR)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🎥 YouTube Idea + Script Generator (Local AI)",
            font=("Arial", 22, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=15)

        # Input Frame
        input_frame = tk.Frame(self.root, bg=BG_COLOR)
        input_frame.pack(pady=10, padx=40, fill="x")

        tk.Label(input_frame, text="Topic / Niche:", bg=BG_COLOR, fg=LABEL_COLOR).pack(
            anchor="w"
        )
        self.topic_entry = tk.Entry(input_frame, font=("Arial", 14), width=80)
        self.topic_entry.pack(pady=5, fill="x")

        tk.Label(input_frame, text="Style:", bg=BG_COLOR, fg=LABEL_COLOR).pack(
            anchor="w", pady=(10, 0)
        )
        self.style_var = tk.StringVar(value="Beginner Friendly")
        styles = [
            "Beginner Friendly",
            "Intermediate",
            "Fun & Energetic",
            "Professional",
            "Storytelling",
        ]
        style_menu = tk.OptionMenu(input_frame, self.style_var, *styles)
        style_menu.pack(anchor="w")

        generate_btn = tk.Button(
            input_frame,
            text="Generate Ideas & Script",
            font=("Arial", 14, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            command=self.generate_content,
        )
        generate_btn.pack(pady=15)

        # Output Area
        output_frame = tk.Frame(self.root, bg=BG_COLOR)
        output_frame.pack(pady=10, padx=40, fill="both", expand=True)

        self.output_text = scrolledtext.ScrolledText(
            output_frame, font=("Arial", 11), height=30, bg="#34495E", fg=TEXT_COLOR
        )
        self.output_text.pack(fill="both", expand=True)

    def generate_content(self):
        topic = self.topic_entry.get().strip()
        style = self.style_var.get()

        if not topic:
            messagebox.showwarning("Input Required", "Please enter a topic!")
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(
            tk.END,
            "Generating with local Llama 3.1...\nThis may take 10-30 seconds.\n\n",
        )

        prompt = f"""You are a professional YouTube content strategist for a Python programming channel.

Topic: "{topic}"
Style: {style}

Generate:
1. 5 catchy video titles (with emojis where appropriate)
2. One SEO-optimized YouTube description (150-200 words, include keywords)
3. Full video script with timestamps (intro, main sections, conclusion, CTA)
4. Detailed thumbnail prompt for AI image generator (Grok Imagine style)

Make it engaging, educational, and suitable for beginner to intermediate Python learners."""

        try:
            response = ollama.chat(
                model="llama3.1", messages=[{"role": "user", "content": prompt}]
            )

            result = response["message"]["content"]

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ollama error: {str(e)}\n\n"
                "Make sure Ollama is running and 'llama3.1' model is installed.\n"
                "Run this in terminal: ollama run llama3.1",
            )

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = YouTubeIdeaGenerator()
    app.run()
