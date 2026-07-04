import tkinter as tk
from tkinter import messagebox, ttk
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import json
import os

# ==================== COLORS ====================
BG_COLOR = "#2C3E50"  # Dark background
TITLE_COLOR = "white"
LABEL_COLOR = "#ECF0F1"  # Light gray
ACCENT_COLOR = "#3498DB"  # Blue
SUCCESS_COLOR = "#2ECC71"  # Green
TEXT_COLOR = "#ECF0F1"
WARNING_COLOR = "red"


class StockTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock Price Tracker - Coding With Nathan")
        self.root.geometry("1000x900")
        self.root.configure(bg=BG_COLOR)

        self.watchlist = []  # List of dicts
        self.create_widgets()
        self.load_watchlist()

    def create_widgets(self):
        # Title
        title = tk.Label(
            self.root,
            text="📈 Live Stock Price Tracker",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        )
        title.pack(pady=15)

        # Search Frame
        search_frame = tk.Frame(self.root, bg=BG_COLOR)
        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Stock Symbol:",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        ).pack(side=tk.LEFT, padx=10)

        self.symbol_entry = tk.Entry(search_frame, font=("Arial", 14), width=15)
        self.symbol_entry.pack(side=tk.LEFT, padx=5)
        self.symbol_entry.bind("<Return>", lambda e: self.get_stock_info())

        search_btn = tk.Button(
            search_frame,
            text="Get Price",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            command=self.get_stock_info,
        )
        search_btn.pack(side=tk.LEFT, padx=10)

        # Results Frame
        self.result_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.result_frame.pack(pady=20, padx=40, fill="x")

        self.info_label = tk.Label(
            self.result_frame,
            text="Enter a stock symbol (e.g. AAPL, TSLA, MSFT)",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=LABEL_COLOR,
        )
        self.info_label.pack(pady=10)

        # Chart Frame
        self.chart_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.chart_frame.pack(pady=10, fill="both", expand=True)

        # Watchlist
        watchlist_frame = tk.Frame(self.root, bg=BG_COLOR)
        watchlist_frame.pack(pady=10, padx=40, fill="x")

        tk.Label(
            watchlist_frame,
            text="Watchlist:",
            font=("Arial", 12, "bold"),
            bg=BG_COLOR,
            fg=TITLE_COLOR,
        ).pack(anchor="w")

        self.watchlist_listbox = tk.Listbox(
            watchlist_frame, font=("Arial", 11), height=8, bg="#34495E", fg=TEXT_COLOR
        )
        self.watchlist_listbox.pack(fill="x", pady=5)
        self.watchlist_listbox.bind("<<ListboxSelect>>", self.on_watchlist_select)

        btn_frame = tk.Frame(watchlist_frame, bg=BG_COLOR)
        btn_frame.pack(pady=5)

        add_to_watch_btn = tk.Button(
            btn_frame,
            text="Add Current",
            font=("Arial", 10),
            bg=ACCENT_COLOR,
            fg="white",
            command=self.add_to_watchlist,
        )
        add_to_watch_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(
            btn_frame,
            text="Delete Selected",
            font=("Arial", 10),
            bg=WARNING_COLOR,
            fg="white",
            command=self.delete_from_watchlist,
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

    def load_watchlist(self):
        """Load watchlist from file if exists."""
        try:
            if os.path.exists("watchlist.json"):
                with open("watchlist.json", "r") as f:
                    self.watchlist = json.load(f)
                    self.refresh_watchlist()
        except:
            self.watchlist = []

    def save_watchlist(self):
        try:
            with open("watchlist.json", "w") as f:
                json.dump(self.watchlist, f)
        except:
            pass

    def refresh_watchlist(self):
        self.watchlist_listbox.delete(0, tk.END)
        for item in self.watchlist:
            display = f"{item['symbol']} - ${item.get('last_price',0):.2f}"
            self.watchlist_listbox.insert(tk.END, display)

    def get_stock_info(self):
        symbol = self.symbol_entry.get().strip().upper()
        if not symbol:
            messagebox.showwarning("Input Required", "Please enter a stock symbol!")
            return

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            price = info.get("currentPrice") or info.get("regularMarketPrice")
            change = info.get("regularMarketChangePercent", 0)
            volume = info.get("regularMarketVolume", 0)
            high_52w = info.get("fiftyTwoWeekHigh", 0)
            low_52w = info.get("fiftyTwoWeekLow", 0)

            self.info_label.config(
                text=f"{symbol} | ${price:.2f} | Change: {change:+.2f}% | "
                f"52w High: ${high_52w:.2f} | 52w Low: ${low_52w:.2f}",
                fg=SUCCESS_COLOR if change >= 0 else WARNING_COLOR,
            )

            # Clear previous chart
            for widget in self.chart_frame.winfo_children():
                widget.destroy()

            # Simple 1-month chart
            hist = ticker.history(period="1mo")
            if not hist.empty:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(hist.index, hist["Close"], color="#34980B")
                ax.set_title(f"{symbol} - Last 1 Month")
                ax.grid(True)

                canvas = FigureCanvasTkAgg(fig, self.chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Could not getch data for {symbol}.\n\nError: {str(e)}"
            )

    def add_to_watchlist(self):
        symbol = self.symbol_entry.get().strip().upper()
        if not symbol:
            return

        # Check if already in watchlist
        if any(item["symbol"] == symbol for item in self.watchlist):
            return

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get("currentPrice") or info.get("regularMarketPrice", 0)
            high_52w = info.get("fiftyTwoWeekHigh", 0)
            low_52w = info.get("fiftyTwoWeekLow", 0)

            self.watchlist.append(
                {
                    "symbol": symbol,
                    "last_price": round(price, 2),
                    "high_52w": round(high_52w, 2),
                    "low_52w": round(low_52w, 2),
                }
            )
            self.save_watchlist()
            self.refresh_watchlist()
        except:
            messagebox.showwarning("Error", f"Could not fetch price for {symbol}")

    def on_watchlist_select(self, event):
        selection = self.watchlist_listbox.curselection()
        if selection:
            index = selection[0]
            symbol = self.watchlist[index]["symbol"]
            self.symbol_entry.delete(0, tk.END)
            self.symbol_entry.insert(0, symbol)

    def delete_from_watchlist(self):
        selection = self.watchlist_listbox.curselection()
        if selection:
            index = selection[0]
            del self.watchlist[index]
            self.save_watchlist()
            self.refresh_watchlist()

    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = StockTracker()
    app.run()
