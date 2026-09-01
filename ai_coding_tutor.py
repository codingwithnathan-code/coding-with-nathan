import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
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
CODE_BG = "#181825"

HISTORY_FILE = "tutor_history.json"


class AICodingTutor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Coding Tutor - Coding With Nathan")
        self.root.geometry("1200x820")
        self.root.configure(bg=BG_COLOR)

        self.last_response = ""
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="AI Coding Tutor (Local Llama)",
            font=("Arial", 22, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=12)

        # Top controls
        control_frame = tk.Frame(self.root, bg=BG_COLOR)
        control_frame.pack(fill="x", padx=20)

        tk.Label(control_frame, text="Task:", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            side=tk.LEFT
        )
        self.mode_var = tk.StringVar(value="Explain and Fix")
        modes = [
            "Explain and Fix",
            "Explain Only",
            "Improve Code",
            "Add Comments",
            "Write Tests",
        ]
        mode_menu = tk.OptionMenu(control_frame, self.mode_var, *modes)
        mode_menu.pack(side=tk.LEFT, padx=8)

        tk.Label(control_frame, text="Language:", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            side=tk.LEFT, padx=(15, 0)
        )
        self.lang_var = tk.StringVar(value="Python")
        lang_menu = tk.OptionMenu(
            control_frame, self.lang_var, "Python", "JavaScript", "C#", "HTML/CSS"
        )
        lang_menu.pack(side=tk.LEFT, padx=8)

        # Main split
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # Left: student code
        left = tk.Frame(main, bg=BG_COLOR)
        left.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 8))

        tk.Label(left, text="Your Code / Error", bg=BG_COLOR, fg=TEXT_COLOR).pack(
            anchor="w"
        )
        self.code_box = scrolledtext.ScrolledText(
            left,
            font=("Consolas", 12),
            bg=CODE_BG,
            fg=TEXT_COLOR,
            wrap=tk.NONE,
            height=18,
        )
        self.code_box.pack(fill="both", expand=True)

        extra_frame = tk.Frame(left, bg=BG_COLOR)
        extra_frame.pack(fill="x", pady=6)
        tk.Label(
            extra_frame,
            text="What is going wrong? (optional)",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        ).pack(anchor="w")
        self.error_entry = tk.Entry(
            extra_frame, font=("Arial", 12), bg=BUTTON_COLOR, fg=TEXT_COLOR
        )
        self.error_entry.pack(fill="x")

        btn_row = tk.Frame(left, bg=BG_COLOR)
        btn_row.pack(fill="x", pady=8)

        tk.Button(
            btn_row,
            text="Ask Tutor",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="#1e1e2e",
            command=self.ask_tutor,
        ).pack(side=tk.LEFT)

        tk.Button(
            btn_row,
            text="Load File",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.load_file,
        ).pack(side=tk.LEFT, padx=8)

        tk.Button(
            btn_row,
            text="Clear",
            font=("Arial", 11),
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.clear_all,
        ).pack(side=tk.LEFT)

        # Right: tutor reply
        right = tk.Frame(main, bg=BG_COLOR)
        right.pack(side=tk.RIGHT, fill="both", expand=True, padx=(8, 0))

        tk.Label(
            right, text="Tutor Explanation + Fixed Code", bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(anchor="w")
        self.output_box = scrolledtext.ScrolledText(
            right,
            font=("Consolas", 11),
            bg=CODE_BG,
            fg=TEXT_COLOR,
            wrap=tk.WORD,
            height=18,
        )
        self.output_box.pack(fill="both", expand=True)

        out_btns = tk.Frame(right, bg=BG_COLOR)
        out_btns.pack(fill="x", pady=8)

        tk.Button(
            out_btns,
            text="Copy Reply",
            font=("Arial", 11),
            bg=SUCCESS_COLOR,
            fg="#1e1e2e",
            command=self.copy_reply,
        ).pack(side=tk.LEFT)

        tk.Button(
            out_btns,
            text="Save Reply",
            font=("Arial", 11),
            bg=WARNING_COLOR,
            fg="#1e1e2e",
            command=self.save_reply,
        ).pack(side=tk.LEFT, padx=8)

        self.status = tk.Label(
            self.root,
            text="Ready • Make sure Ollama is running (ollama run llama3.1)",
            bg=BG_COLOR,
            fg="#6c7086",
            font=("Arial", 10),
        )
        self.status.pack(pady=6)

        self.code_box.insert(
            "1.0",
            'print("Hello World"\n# Paste broken code here',
        )

    def build_prompt(self, code, extra, mode, language):
        instructions = {
            "Explain and Fix": (
                "1. Explain the problem in simple beginner language.\n"
                "2. Show the corrected code.\n"
                "3. Briefly explain why the fix works."
            ),
            "Explain Only": (
                "Explain what this code does and any problems it has.\n"
                "Do not rewrite the whole file unless needed."
            ),
            "Improve Code": (
                "Improve this code for beginners: clearer names, simpler structure, and comments.\n"
                "Then explain the improvements."
            ),
            "Add Comments": (
                "Add clear beginner-friendly comments to the code.\n"
                "Return the fully commented code."
            ),
            "Write Tests": (
                "Explain the code briefly, then write simple tests a beginner could run."
            ),
        }

        prompt = f"""You are a friendly coding tutor for beginners.

    IMPORTANT:
    The student HAS already provided code below.
    Do not say the student forgot to paste code.
    Do not ask them to paste code again.
    Use the code between START_CODE and END_CODE.

    Language: {language}
    Task: {mode}

    Extra notes from the student:
    {extra if extra else "None"}

    START_CODE
    {code}
    END_CODE

    Your job:
    {instructions[mode]}

    Keep the explanation short and easy to follow.
    Never mention that you are an AI.
    """
        return prompt

    def ask_tutor(self):
        code = self.code_box.get("1.0", tk.END).strip()
        print("CODE BEING SENT:")
        print(code)
        print("-----")
        extra = self.error_entry.get().strip()
        mode = self.mode_var.get()
        language = self.lang_var.get()

        if not code:
            messagebox.showwarning("Missing Code", "Please paste some code first.")
            return

        self.status.config(text="Tutor is thinking...")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(
            "1.0", "Asking local Llama...\nThis may take 10-30 seconds."
        )
        self.root.update()

        prompt = self.build_prompt(code, extra, mode, language)

        try:
            response = ollama.chat(
                model="gemma4:26b",
                messages=[{"role": "user", "content": prompt}],
            )
            reply = response["message"]["content"].strip()
            self.last_response = reply

            self.output_box.delete("1.0", tk.END)
            self.output_box.insert("1.0", reply)
            self.status.config(text="Done")
            self.save_history(code, extra, mode, reply)

        except Exception as e:
            self.status.config(text="Error")
            messagebox.showerror(
                "Ollama Error",
                "Could not reach local Llama.\n\n"
                "Make sure Ollama is running:\n"
                "ollama run llama3.1\n\n"
                f"Error: {e}",
            )

    def load_file(self):
        path = filedialog.askopenfilename(
            title="Open code file",
            filetypes=[
                ("Python files", "*.py"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.code_box.delete("1.0", tk.END)
            self.code_box.insert("1.0", content)
            self.status.config(text=f"Loaded {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("File Error", str(e))

    def clear_all(self):
        self.code_box.delete("1.0", tk.END)
        self.error_entry.delete(0, tk.END)
        self.output_box.delete("1.0", tk.END)
        self.status.config(text="Cleared")

    def copy_reply(self):
        text = self.output_box.get("1.0", tk.END).strip()
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status.config(text="Copied tutor reply")

    def save_reply(self):
        text = self.output_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Save", "No tutor reply to save.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        self.status.config(text="Reply saved")

    def save_history(self, code, extra, mode, reply):
        item = {
            "time": datetime.now().isoformat(),
            "mode": mode,
            "extra": extra,
            "code": code[:2000],
            "reply": reply[:4000],
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
    app = AICodingTutor()
    app.run()
