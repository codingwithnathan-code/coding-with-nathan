import tkinter as tk
from tkinter import messagebox, scrolledtext
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
WARNING_COLOR = "#f9e2af"
BUTTON_COLOR = "#313244"
BOX_BG = "#181825"

HISTORY_FILE = "email_rewrites.json"


class AIEmailRewriter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Email Rewriter - Coding With Nathan")
        self.root.geometry("1100x800")
        self.root.configure(bg=BG_COLOR)

        self.last_rewrite = ""
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="AI Email Rewriter",
            font=("Arial", 22, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=12)

        settings = tk.Frame(self.root, bg=BG_COLOR)
        settings.pack(fill="x", padx=20)

        tk.Label(settings, text="Style:", bg=BG_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT)
        self.style_var = tk.StringVar(value="Professional")
        styles = [
            "Professional",
            "Short and Clear",
            "Friendly",
            "Polite Follow-Up",
            "Firm but Respectful",
        ]
        tk.OptionMenu(settings, self.style_var, *styles).pack(side=tk.LEFT, padx=8)

        tk.Label(settings, text="Your name:", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            side=tk.LEFT, padx=(15, 0)
        )
        self.name_entry = tk.Entry(
            settings,
            font=("Arial", 12),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            width=18,
        )
        self.name_entry.insert(0, "Nathan")
        self.name_entry.pack(side=tk.LEFT, padx=8)

        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        left = tk.Frame(main, bg=BG_COLOR)
        left.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 8))

        tk.Label(left, text="Rough email", bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w")
        self.draft_box = scrolledtext.ScrolledText(
            left, font=("Arial", 12), bg=BOX_BG, fg=TEXT_COLOR, wrap=tk.WORD, height=18
        )
        self.draft_box.pack(fill="both", expand=True)
        self.draft_box.insert(
            "1.0",
            "hey i still havent got the file you said you would send yesterday. "
            "need it today if possible. thanks",
        )

        left_btns = tk.Frame(left, bg=BG_COLOR)
        left_btns.pack(fill="x", pady=8)

        tk.Button(
            left_btns,
            text="Rewrite Email",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="#1e1e2e",
            command=self.rewrite_email,
        ).pack(side=tk.LEFT)

        tk.Button(
            left_btns,
            text="Clear Draft",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.clear_draft,
        ).pack(side=tk.LEFT, padx=8)

        right = tk.Frame(main, bg=BG_COLOR)
        right.pack(side=tk.RIGHT, fill="both", expand=True, padx=(8, 0))

        tk.Label(right, text="Rewritten email", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            anchor="w"
        )
        self.output_box = scrolledtext.ScrolledText(
            right, font=("Arial", 12), bg=BOX_BG, fg=TEXT_COLOR, wrap=tk.WORD, height=18
        )
        self.output_box.pack(fill="both", expand=True)

        right_btns = tk.Frame(right, bg=BG_COLOR)
        right_btns.pack(fill="x", pady=8)

        tk.Button(
            right_btns,
            text="Copy Rewrite",
            font=("Arial", 11),
            bg=SUCCESS_COLOR,
            fg="#1e1e2e",
            command=self.copy_rewrite,
        ).pack(side=tk.LEFT)

        tk.Button(
            right_btns,
            text="Save Rewrite",
            font=("Arial", 11),
            bg=WARNING_COLOR,
            fg="#1e1e2e",
            command=self.save_rewrite,
        ).pack(side=tk.LEFT, padx=8)

        self.status = tk.Label(
            self.root,
            text="Paste a rough email and click Rewrite Email",
            bg=BG_COLOR,
            fg="#6c7086",
            font=("Arial", 10),
        )
        self.status.pack(pady=6)

    def build_prompt(self, draft, style, name):
        return f"""You rewrite emails for a beginner-friendly writing helper.

Style: {style}
Sign the email as: {name}

Rough email:
START_EMAIL
{draft}
END_EMAIL

Rules:
- Keep the same meaning. Do not invent facts.
- Do not add a fake company name or phone number.
- Use a clear subject line, then the email body.
- Keep it natural. Do not sound robotic.
- Do not mention that you are an AI.

Use this exact format:

SUBJECT: [subject line]
BODY:
[email body]
"""

    def rewrite_email(self):
        draft = self.draft_box.get("1.0", tk.END).strip()
        if not draft:
            messagebox.showwarning("Missing Email", "Please paste a rough email first.")
            return

        style = self.style_var.get()
        name = self.name_entry.get().strip() or "Nathan"

        self.status.config(text="Rewriting with local Llama...")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(
            "1.0", "Rewriting email...\nThis may take 10-30 seconds."
        )
        self.root.update()

        prompt = self.build_prompt(draft, style, name)

        try:
            response = ollama.chat(
                model="gemma4:26b",
                messages=[{"role": "user", "content": prompt}],
            )
            rewrite = response["message"]["content"].strip()
            self.last_rewrite = rewrite

            self.output_box.delete("1.0", tk.END)
            self.output_box.insert("1.0", rewrite)
            self.status.config(text=f"Rewrite complete ({style})")
            self.save_history(draft, style, rewrite)

        except Exception as e:
            messagebox.showerror(
                "Ollama Error",
                "Could not reach local Llama.\n\n"
                "Make sure Ollama is running:\n"
                "ollama run llama3.1\n\n"
                f"Error: {e}",
            )
            self.status.config(text="Error - check Ollama")

    def clear_draft(self):
        self.draft_box.delete("1.0", tk.END)
        self.status.config(text="Draft cleared")

    def copy_rewrite(self):
        text = self.output_box.get("1.0", tk.END).strip()
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status.config(text="Rewrite copied")

    def save_rewrite(self):
        text = self.output_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Save", "No rewrite to save.")
            return
        filename = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("Saved", f"Saved to {filename}")

    def save_history(self, draft, style, rewrite):
        item = {
            "time": datetime.now().isoformat(),
            "style": style,
            "draft": draft,
            "rewrite": rewrite,
        }
        history = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = []
        history.append(item)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history[-50:], f, indent=2)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIEmailRewriter()
    app.run()
