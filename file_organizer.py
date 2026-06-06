import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from collections import defaultdict

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
SUCCESS_COLOR = "#2ECC71"  # Green
TEXT_COLOR = "#ECF0F1"


class FileOrganizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Organizer - Coding With Nathan")
        self.root.geometry("800x600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.selected_folder = ""
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="File Organizer",
            font=("Arial", 26, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=20)

        tk.Label(
            self.root,
            text="Sort files automatically by their type",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        ).pack(pady=5)

        # Select Folder Button
        select_btn = tk.Button(
            self.root,
            text="Select Folder",
            font=("Arial", 14, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            width=20,
            height=2,
            command=self.select_folder,
        )
        select_btn.pack(pady=20)

        # Selected Folder Display
        self.folder_label = tk.Label(
            self.root,
            text="No folder selected",
            font=("Arial", 11),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
            wraplength=700,
        )
        self.folder_label.pack(pady=10, padx=40)

        # Organize Button
        self.organize_btn = tk.Button(
            self.root,
            text="Organize Files",
            font=("Arial", 14, "bold"),
            bg=SUCCESS_COLOR,
            fg="white",
            width=25,
            height=2,
            state="disabled",
            command=self.organize_files,
        )
        self.organize_btn.pack(pady=20)

        # Progress / Log Area
        tk.Label(
            self.root,
            text="Progress Log:",
            font=("Arial", 12, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        ).pack(anchor="w", padx=40, pady=5)

        self.log_text = tk.Text(
            self.root, font=("Arial", 10), height=18, bg="#34495E", fg=TEXT_COLOR
        )
        self.log_text.pack(pady=10, padx=40, fill="both", expand=True)

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        if self.selected_folder:
            self.folder_label.config(text=f"Selected Folder : {self.selected_folder}")
            self.organize_btn.config(state="normal")
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "Folder selected. Ready to organize.\n")

    def organize_files(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(
            tk.END, f"Starting organization of:\n{self.selected_folder}\n\n"
        )

        # File type categories
        file_categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Documents": [
                ".pdf",
                ".doc",
                ".docx",
                ".txt",
                ".ppt",
                "pptx",
                ".xls",
                ".xlsx",
            ],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
            "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go"],
        }

        moved_count = 0
        category_count = defaultdict(int)

        try:
            # Get all files in the folder
            for filename in os.listdir(self.selected_folder):
                file_path = os.path.join(self.selected_folder, filename)

                # Skip if it's a folder
                if os.path.isdir(file_path):
                    continue

                file_ext = os.path.splitext(filename)[1].lower()

                # Find which category this file belongs to
                moved = False
                for category, extensions in file_categories.items():
                    if file_ext in extensions:
                        destination_dir = os.path.join(self.selected_folder, category)
                        os.makedirs(destination_dir, exist_ok=True)

                        shutil.move(file_path, os.path.join(destination_dir, filename))
                        self.log_text.insert(
                            tk.END, f"Moved: {filename} -> {category}/\n"
                        )
                        moved_count += 1
                        category_count[category] += 1
                        moved = True
                        break

                # If no category matched, put in "Others"
                if not moved:
                    others_dir = os.path.join(self.selected_folder, "Others")
                    os.makedirs(others_dir, exist_ok=True)
                    shutil.move(file_path, os.path.join(others_dir, filename))
                    self.log_text.insert(tk.END, f"Moved: {filename} -> Others/\n")
                    moved_count += 1
                    category_count["Others"] += 1

            # Final Summary
            self.log_text.insert(tk.END, "\n" + "=" * 50 + "\n")
            self.log_text.insert(tk.END, f"ORGANIZATION COMPLETE!\n")
            self.log_text.insert(tk.END, f"Total files moved: {moved_count}\n\n")

            for category, count in category_count.items():
                self.log_text.insert(tk.END, f"{category}: {count} files\n")

            messagebox.showinfo(
                "Success", f"Successfully organized {moved_count} files!"
            )

        except Exception as e:
            messagebox.showerror("Error", f"An error occured: {str(e)}")

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = FileOrganizer()
    app.run()
