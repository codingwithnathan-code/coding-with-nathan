import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
import base64
import os
import datetime
from io import BytesIO
from moviepy import ImageClip
import numpy as np
import time

# ==================== CONFIG ====================
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY_HERE"  # ← Put your key here

OUTPUT_IMAGES_DIR = "generated_images"
OUTPUT_VIDEOS_DIR = "looping_videos"
LOG_FILE = "generation_log.txt"

os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_VIDEOS_DIR, exist_ok=True)

MODELS = {
    "Seedream 4.5 (Recommended)": "bytedance-seed/seedream-4.5",
    "Gemini 2.5 Flash Image": "google/gemini-2.5-flash-image",
    "Gemini 3.1 Flash Image": "google/gemini-3.1-flash-image",
    "FLUX.2 Pro": "black-forest-labs/flux.2-pro",
}


class ImageToLoopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Image → Looping Video Generator - Coding With Nathan")
        self.root.geometry("1100x850")
        self.root.configure(bg="#1e1e2e")

        self.generated_images = []
        self.create_widgets()

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[{timestamp}] {message}")

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="AI Image → Seamless Looping Video",
            font=("Arial", 22, "bold"),
            bg="#1e1e2e",
            fg="white",
        )
        title.pack(pady=15)

        input_frame = tk.Frame(self.root, bg="#1e1e2e")
        input_frame.pack(pady=10, padx=30, fill="x")

        tk.Label(input_frame, text="Prompt:", bg="#1e1e2e", fg="#cdd6f4").pack(
            anchor="w"
        )
        self.prompt_entry = tk.Entry(input_frame, font=("Arial", 13), width=90)
        self.prompt_entry.pack(pady=5, fill="x")

        control_frame = tk.Frame(input_frame, bg="#1e1e2e")
        control_frame.pack(fill="x", pady=10)

        tk.Label(control_frame, text="Model:", bg="#1e1e2e", fg="#cdd6f4").pack(
            side=tk.LEFT
        )
        self.model_var = tk.StringVar(value=list(MODELS.keys())[0])
        ttk.Combobox(
            control_frame,
            textvariable=self.model_var,
            values=list(MODELS.keys()),
            width=38,
            state="readonly",
        ).pack(side=tk.LEFT, padx=8)

        tk.Label(control_frame, text="# of Images:", bg="#1e1e2e", fg="#cdd6f4").pack(
            side=tk.LEFT, padx=(15, 5)
        )
        self.num_images_var = tk.StringVar(value="2")
        ttk.Combobox(
            control_frame,
            textvariable=self.num_images_var,
            values=["1", "2", "3", "4"],
            width=5,
            state="readonly",
        ).pack(side=tk.LEFT)

        tk.Button(
            control_frame,
            text="Generate Images",
            font=("Arial", 12, "bold"),
            bg="#89b4fa",
            fg="#1e1e2e",
            command=self.generate_images,
        ).pack(side=tk.LEFT, padx=15)

        self.preview_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.preview_frame.pack(pady=10, fill="both", expand=True)

        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=15)

        self.create_videos_btn = tk.Button(
            btn_frame,
            text="Create Looping Videos from Approved",
            font=("Arial", 13, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            command=self.create_looping_videos,
            state="disabled",
        )
        self.create_videos_btn.pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="Clear All",
            font=("Arial", 11),
            bg="#f38ba8",
            fg="white",
            command=self.clear_all,
        ).pack(side=tk.LEFT, padx=10)

    def generate_images(self):
        prompt = self.prompt_entry.get().strip()
        if not prompt:
            messagebox.showwarning("Missing Prompt", "Please enter a prompt!")
            return

        if OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY_HERE":
            messagebox.showerror(
                "API Key Missing", "Please add your OpenRouter API key."
            )
            return

        model_name = MODELS[self.model_var.get()]
        num_images = int(self.num_images_var.get())

        self.clear_preview()
        self.log(f"START → Generating {num_images} image(s) with {model_name}")
        messagebox.showinfo(
            "Generating", f"Generating {num_images} image(s)...\nThis may take a while."
        )

        success_count = 0

        for i in range(num_images):
            try:
                self.log(f"REQUEST #{i+1} → {model_name} | Prompt: {prompt}")

                # Minimal payload that works with most models
                payload = {
                    "model": model_name,
                    "prompt": prompt,
                    "n": 1,  # Force n=1 for compatibility
                }

                # Only add extra params for Seedream (it supports them better)
                if "seedream" in model_name:
                    payload["aspect_ratio"] = "16:9"
                    payload["output_format"] = "png"

                response = requests.post(
                    "https://openrouter.ai/api/v1/images",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://codingwithnathan.com",
                        "X-Title": "Coding With Nathan",
                    },
                    json=payload,
                    timeout=90,
                )

                if response.status_code != 200:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    self.log(f"ERROR #{i+1} → {error_msg}")
                    continue

                data = response.json()
                images_data = data.get("data", [])

                if not images_data:
                    self.log(f"ERROR #{i+1} → No image returned")
                    continue

                img_obj = images_data[0]
                b64 = img_obj.get("b64_json") or img_obj.get("base64")
                if not b64:
                    self.log(f"ERROR #{i+1} → No base64 data")
                    continue

                img_bytes = base64.b64decode(b64)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{OUTPUT_IMAGES_DIR}/img_{timestamp}_{i+1}.png"

                with open(filename, "wb") as f:
                    f.write(img_bytes)

                self.log(f"SAVED #{i+1} → {filename}")

                pil_img = Image.open(BytesIO(img_bytes))
                pil_img.thumbnail((380, 220))
                photo = ImageTk.PhotoImage(pil_img)

                self.generated_images.append(
                    {
                        "path": filename,
                        "photo": photo,
                        "approved": False,
                    }
                )
                success_count += 1

                # Small delay between requests
                time.sleep(1.2)

            except Exception as e:
                self.log(f"EXCEPTION #{i+1} → {str(e)}")

        if success_count > 0:
            self.display_images()
            self.create_videos_btn.config(state="normal")
            messagebox.showinfo(
                "Done", f"Successfully generated {success_count} image(s)!"
            )
        else:
            messagebox.showerror("Failed", "No images were generated. Check the log.")

    def display_images(self):
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        for idx, item in enumerate(self.generated_images):
            frame = tk.Frame(self.preview_frame, bg="#313244", padx=10, pady=10)
            frame.grid(row=idx // 2, column=idx % 2, padx=15, pady=15)

            label = tk.Label(frame, image=item["photo"], bg="#313244")
            label.image = item["photo"]
            label.pack()

            status = tk.Label(frame, text="Not Approved", bg="#313244", fg="#f38ba8")
            status.pack(pady=5)

            btn_frame = tk.Frame(frame, bg="#313244")
            btn_frame.pack()

            def make_approve(i=idx, s=status):
                def approve():
                    self.generated_images[i]["approved"] = True
                    s.config(text="✓ Approved", fg="#a6e3a1")

                return approve

            def make_reject(i=idx, s=status):
                def reject():
                    self.generated_images[i]["approved"] = False
                    s.config(text="Not Approved", fg="#f38ba8")

                return reject

            tk.Button(
                btn_frame, text="Approve", bg="#a6e3a1", command=make_approve()
            ).pack(side=tk.LEFT, padx=5)
            tk.Button(
                btn_frame, text="Reject", bg="#f38ba8", command=make_reject()
            ).pack(side=tk.LEFT, padx=5)

    def create_looping_videos(self):
        approved = [img for img in self.generated_images if img["approved"]]
        if not approved:
            messagebox.showwarning(
                "None Approved", "Please approve at least one image first."
            )
            return

        for i, item in enumerate(approved):
            try:
                self.make_seamless_loop(item["path"], i)
                self.log(f"VIDEO CREATED → {item['path']}")
            except Exception as e:
                self.log(f"VIDEO ERROR → {str(e)}")
                messagebox.showerror("Video Error", f"Failed on image {i+1}: {e}")

        messagebox.showinfo("Done!", f"Created {len(approved)} looping videos!")

    def make_seamless_loop(self, image_path, index):
        duration = 6
        fps = 24
        clip = ImageClip(image_path).with_duration(duration)

        def make_frame(get_frame, t):
            img = get_frame(t)
            h, w = img.shape[:2]
            progress = t / duration
            scale = 1.0 + 0.15 * progress
            x_shift = int(25 * np.sin(progress * np.pi))

            new_w = int(w * scale)
            new_h = int(h * scale)

            from PIL import Image as PILImage

            pil_img = PILImage.fromarray(img)
            pil_img = pil_img.resize((new_w, new_h), PILImage.LANCZOS)

            left = max(0, min((new_w - w) // 2 + x_shift, new_w - w))
            top = max(0, min((new_h - h) // 2, new_h - h))

            return np.array(pil_img.crop((left, top, left + w, top + h)))

        animated = clip.transform(make_frame)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{OUTPUT_VIDEOS_DIR}/loop_{timestamp}_{index+1}.mp4"

        animated.write_videofile(
            output_path,
            fps=fps,
            codec="libx264",
            audio=False,
            preset="medium",
            threads=4,
            logger=None,
        )

    def clear_preview(self):
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        self.generated_images = []
        self.create_videos_btn.config(state="disabled")

    def clear_all(self):
        self.clear_preview()
        self.prompt_entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ImageToLoopApp()
    app.run()
