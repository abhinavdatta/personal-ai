import tkinter as tk
import win32gui, win32con
import time
import threading
import subprocess

from engine.qa_engine import answer, set_model, get_model
from ui.voice import listen_and_answer


class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#111")

        self.frame = tk.Frame(self.root, bg="#111")
        self.frame.pack(padx=12, pady=10)

        # Title
        tk.Label(
            self.frame,
            text="StudyAI Assistant",
            fg="#00c8ff",
            bg="#111",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        # Status
        self.status = tk.Label(
            self.frame,
            text="Ready",
            fg="#aaa",
            bg="#111",
            font=("Segoe UI", 9)
        )
        self.status.pack(anchor="w", pady=(2, 6))

        # -------------------------
        # Model selector
        # -------------------------
        models = self._load_models()
        self.model_var = tk.StringVar(value=get_model())

        model_frame = tk.Frame(self.frame, bg="#111")
        model_frame.pack(anchor="w", pady=(0, 6))

        tk.Label(
            model_frame,
            text="Model:",
            fg="#aaa",
            bg="#111",
            font=("Segoe UI", 9)
        ).pack(side="left")

        self.model_menu = tk.OptionMenu(
            model_frame,
            self.model_var,
            *models,
            command=self._on_model_change
        )
        self.model_menu.config(bg="#222", fg="white", relief="flat")
        self.model_menu.pack(side="left", padx=6)

        # -------------------------
        # Input field
        # -------------------------
        self.entry = tk.Entry(self.frame, font=("Segoe UI", 11), width=45)
        self.entry.pack(pady=4)
        self.entry.bind("<Return>", self.ask_question)

        # Buttons
        btn_frame = tk.Frame(self.frame, bg="#111")
        btn_frame.pack(pady=4)

        tk.Button(
            btn_frame,
            text="Ask",
            command=self.ask_question,
            bg="#00c8ff",
            fg="black",
            relief="flat",
            padx=10
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame,
            text="Voice",
            command=self.voice_question,
            bg="#444",
            fg="white",
            relief="flat",
            padx=10
        ).pack(side="left", padx=4)

        # Response label
        # Scrollable response area
        text_frame = tk.Frame(self.frame, bg="#111")
        text_frame.pack(fill="both", expand=True, pady=6)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            text_frame,
            height=6,
            wrap="word",
            bg="#111",
            fg="white",
            font=("Segoe UI", 11),
            relief="flat",
            yscrollcommand=scrollbar.set
        )
        self.text_area.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.text_area.yview)


        self.root.geometry("520x260+700+40")
        self.root.update_idletasks()

        hwnd = win32gui.GetParent(self.root.winfo_id())
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        style |= win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_TOPMOST
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

        try:
            WDA_EXCLUDEFROMCAPTURE = 0x11
            win32gui.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        except Exception as e:
            print("Stealth mode not supported:", e)


        self.last_activity = time.time()

        # Activity tracking
        self.root.bind("<Enter>", self._on_activity)
        self.root.bind("<Motion>", self._on_activity)
        self.root.bind("<Key>", self._on_activity)
        self.entry.bind("<Key>", self._on_activity)

        self._schedule_auto_hide()

    # -------------------------
    # Model handling
    # -------------------------
    def _load_models(self):
        try:
            result = subprocess.check_output(["ollama", "list"]).decode()
            lines = result.split("\n")[1:]
            models = []

            for line in lines:
                if line.strip():
                    models.append(line.split()[0])

            return models
        except:
            return ["mistral:latest"]

    def _on_model_change(self, value):
        set_model(value)
        self.set_status(f"Model: {value}")

    # -------------------------
    # AI interaction
    # -------------------------
    def ask_question(self, event=None):
        question = self.entry.get().strip()
        if not question:
            return

        self.set_status("Thinking...")
        self.show("")

        def worker():
            try:
                response = answer(question)
                self.show(response)
                self.set_status("Ready")
            except Exception as e:
                self.show(f"Error: {e}")
                self.set_status("Error")

        threading.Thread(target=worker, daemon=True).start()

    def voice_question(self):
        self.set_status("Listening...")

        def worker():
            listen_and_answer()
            self.set_status("Ready")

        threading.Thread(target=worker, daemon=True).start()

     # -------------------------
    # UI helpers
    # -------------------------
    def show(self, text):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        self.root.deiconify()
        self.last_activity = time.time()

    def set_status(self, text):
        self.status.config(text=text)

    def toggle(self):
        if self.root.state() == "withdrawn":
            self.root.deiconify()
        else:
            self.root.withdraw()

    def _on_activity(self, event=None):
        self.last_activity = time.time()

    def _schedule_auto_hide(self):
        if time.time() - self.last_activity > 30:
            self.root.withdraw()
        self.root.after(1000, self._schedule_auto_hide)
