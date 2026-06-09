import tkinter as tk
from tkinter import messagebox
import requests

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
SUCCESS_COLOR = "#2ECC71"  # Green
TEXT_COLOR = "#ECF0F1"


class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather App - Coding With Nathan")
        self.root.geometry("700x500")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="🌤️ Weather App",
            font=("Arial", 26, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=20)

        # Search Frame
        search_frame = tk.Frame(self.root, bg=BG_COLOR)
        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Enter City:",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        ).pack(side=tk.LEFT, padx=10)

        self.city_entry = tk.Entry(search_frame, font=("Arial", 14), width=25)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.bind(
            "<Return>", lambda e: self.get_weather()
        )  # Press Enter to search

        search_btn = tk.Button(
            search_frame,
            text="Get Weather",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            command=self.get_weather,
        )
        search_btn.pack(side=tk.LEFT, padx=10)

        # Weather Display Frame
        self.info_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.info_frame.pack(pady=30, padx=40, fill="both", expand=True)

        # Default message
        self.default_label = tk.Label(
            self.info_frame,
            text="Enter a city name to get weather information",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        )
        self.default_label.pack(pady=50)

        # Results labels (hidden initially)
        self.city_label = tk.Label(
            self.info_frame,
            text="",
            font=("Arial", 18, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        self.temp_label = tk.Label(
            self.info_frame,
            text="",
            font=("Arial", 48, "bold"),
            bg=BG_COLOR,
            fg=SUCCESS_COLOR,
        )
        self.condition_label = tk.Label(
            self.info_frame, text="", font=("Arial", 16), bg=BG_COLOR, fg=LABEL_COLOR
        )
        self.details_label = tk.Label(
            self.info_frame,
            text="",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
            justify="left",
        )

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name!")
            return

        try:
            # First get coordinates using Open-Meteo Geocoding
            geo_url = (
                f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            )
            geo_response = requests.get(geo_url)
            geo_data = geo_response.json()

            if "results" not in geo_data or not geo_data["results"]:
                messagebox.showerror(
                    "City Not Found", f"Could not find weather for '{city}'"
                )
                return

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            city_name = geo_data["results"][0]["name"]

            # Get current weather
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            current = weather_data["current"]

            # Weather code to description mapping
            weather_codes = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Parly cloudy",
                3: "Overcaset",
                45: "Fog",
                48: "Depositing rime fog",
                51: "Light drizzle",
                53: "Moderate drizzle",
                55: "Dense drizzle",
                61: "Slight rain",
                63: "Moderate rain",
                65: "Heavy rain",
                71: "Slight snow",
                73: "Moderate snow",
                75: "Heavy snow",
                80: "Slight rain showers",
                81: "Moderate rain showers",
                82: "Violent rain showers",
            }

            codition = weather_codes.get(current["weather_code"], "Unknown")

            # Update GUI
            self.default_label.pack_forget()

            self.city_label.config(text=f"{city_name}")
            self.city_label.pack(pady=10)

            self.temp_label.config(text=f"{current['temperature_2m']} deg C")
            self.temp_label.pack(pady=5)

            self.condition_label.config(text=codition)
            self.condition_label.pack(pady=5)

            details = (
                f"Humidity: {current['relative_humidity_2m']}%\n"
                f"Wind Speed: {current['wind_speed_10m']} km/h"
            )
            self.details_label.config(text=details)
            self.details_label.pack(pady=20)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to fetch weather data.\n\nError: {str(e)}"
            )

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = WeatherApp()
    app.run()
