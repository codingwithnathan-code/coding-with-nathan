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

HISTORY_FILE = "comment_replies.json"


class YouTubeCommentHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Comment Responder Helper - Coding With Nathan")
        self.root.geometry("1150x820")
        self.root.configure(bg=BG_COLOR)

        self.last_replies = ""
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="YouTube Comment Responder Helper",
            font=("Arial", 22, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=12)

        # Settings row
        settings = tk.Frame(self.root, bg=BG_COLOR)
        settings.pack(fill="x", padx=20)

        tk.Label(settings, text="Tone:", bg=BG_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT)
        self.tone_var = tk.StringVar(value="Friendly Teacher")
        tones = [
            "Friendly Teacher",
            "Short and Casual",
            "Thankful and Humble",
            "Helpful and Clear",
            "Funny but Polite",
        ]
        tk.OptionMenu(settings, self.tone_var, *tones).pack(side=tk.LEFT, padx=8)

        tk.Label(settings, text="Channel name:", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            side=tk.LEFT, padx=(15, 0)
        )
        self.channel_entry = tk.Entry(
            settings,
            font=("Arial", 12),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            width=22,
        )
        self.channel_entry.insert(0, "Coding With Nathan")
        self.channel_entry.pack(side=tk.LEFT, padx=8)

        tk.Label(settings, text="Video topic:", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            side=tk.LEFT
        )
        self.topic_entry = tk.Entry(
            settings,
            font=("Arial", 12),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            width=24,
        )
        self.topic_entry.insert(0, "Python tutorial")
        self.topic_entry.pack(side=tk.LEFT, padx=8)

        # Main split
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: comments
        left = tk.Frame(main, bg=BG_COLOR)
        left.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 8))

        tk.Label(
            left, text="Paste comments (one per line)", bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(anchor="w")
        self.comment_box = scrolledtext.ScrolledText(
            left, font=("Arial", 12), bg=BOX_BG, fg=TEXT_COLOR, wrap=tk.WORD, height=18
        )
        self.comment_box.pack(fill="both", expand=True)
        self.comment_box.insert(
            "1.0",
            "This helped me finally understand lists!\n"
            "Can you make a video on dictionaries next?\n"
            "I got an error on line 12.\n"
            "First video I watched. Subscribed.",
        )

        left_btns = tk.Frame(left, bg=BG_COLOR)
        left_btns.pack(fill="x", pady=8)

        tk.Button(
            left_btns,
            text="Generate Replies",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="#1e1e2e",
            command=self.generate_replies,
        ).pack(side=tk.LEFT)

        tk.Button(
            left_btns,
            text="Clear Comments",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.clear_comments,
        ).pack(side=tk.LEFT, padx=8)

        # Right: replies
        right = tk.Frame(main, bg=BG_COLOR)
        right.pack(side=tk.RIGHT, fill="both", expand=True, padx=(8, 0))

        tk.Label(right, text="Suggested replies", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            anchor="w"
        )
        self.reply_box = scrolledtext.ScrolledText(
            right, font=("Arial", 12), bg=BOX_BG, fg=TEXT_COLOR, wrap=tk.WORD, height=18
        )
        self.reply_box.pack(fill="both", expand=True)

        right_btns = tk.Frame(right, bg=BG_COLOR)
        right_btns.pack(fill="x", pady=8)

        tk.Button(
            right_btns,
            text="Copy All Replies",
            font=("Arial", 11),
            bg=SUCCESS_COLOR,
            fg="#1e1e2e",
            command=self.copy_replies,
        ).pack(side=tk.LEFT)

        tk.Button(
            right_btns,
            text="Save Replies",
            font=("Arial", 11),
            bg=WARNING_COLOR,
            fg="#1e1e2e",
            command=self.save_replies,
        ).pack(side=tk.LEFT, padx=8)

        self.status = tk.Label(
            self.root,
            text="Paste comments and click Generate Replies",
            bg=BG_COLOR,
            fg="#6c7086",
            font=("Arial", 10),
        )
        self.status.pack(pady=6)

    def get_comments(self):
        raw = self.comment_box.get("1.0", tk.END)
        comments = []
        for line in raw.splitlines():
            line = line.strip()
            if line:
                comments.append(line)
        return comments

    def build_prompt(self, comments, tone, channel, topic):
        numbered = ""
        for i, comment in enumerate(comments, start=1):
            numbered += f"{i}. {comment}\n"

        prompt = f"""You write YouTube comment replies for a coding channel.

Channel name: {channel}
Video topic: {topic}
Tone: {tone}

Write one reply for each comment below.
Use this exact format:

COMMENT: [the original comment]
REPLY: [your reply]

Rules:
- Keep each reply short, 1 to 3 sentences.
- Sound like a real creator, not a robot.
- Be polite, even if the comment is negative.
- If they ask for a future video, thank them and say it is a good idea.
- If they mention an error, ask for the exact error message.
- Do not use hashtags.
- Do not mention that you are an AI.
- Create exactly one reply per comment.

Comments:
{numbered}
"""
        return prompt

    def generate_replies(self):
        comments = self.get_comments()
        if not comments:
            messagebox.showwarning(
                "Missing Comments", "Please paste at least one comment."
            )
            return

        tone = self.tone_var.get()
        channel = self.channel_entry.get().strip() or "Coding With Nathan"
        topic = self.topic_entry.get().strip() or "Python tutorial"

        self.status.config(text="Writing replies with local Llama...")
        self.reply_box.delete("1.0", tk.END)
        self.reply_box.insert(
            "1.0", "Generating replies...\nThis may take 10-30 seconds."
        )
        self.root.update()

        prompt = self.build_prompt(comments, tone, channel, topic)

        try:
            response = ollama.chat(
                model="gemma4:26b",
                messages=[{"role": "user", "content": prompt}],
            )
            reply_text = response["message"]["content"].strip()
            self.last_replies = reply_text

            self.reply_box.delete("1.0", tk.END)
            self.reply_box.insert("1.0", reply_text)
            self.status.config(text=f"Created replies for {len(comments)} comment(s)")
            self.save_history(comments, tone, reply_text)

        except Exception as e:
            messagebox.showerror(
                "Ollama Error",
                "Could not reach local Llama.\n\n"
                "Make sure Ollama is running:\n"
                "ollama run llama3.1\n\n"
                f"Error: {e}",
            )
            self.status.config(text="Error - check Ollama")

    def clear_comments(self):
        self.comment_box.delete("1.0", tk.END)
        self.status.config(text="Comments cleared")

    def copy_replies(self):
        text = self.reply_box.get("1.0", tk.END).strip()
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status.config(text="Replies copied")

    def save_replies(self):
        text = self.reply_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Save", "No replies to save.")
            return

        filename = f"replies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("Saved", f"Saved to {filename}")

    def save_history(self, comments, tone, replies):
        item = {
            "time": datetime.now().isoformat(),
            "tone": tone,
            "comments": comments,
            "replies": replies,
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
    app = YouTubeCommentHelper()
    app.run()
