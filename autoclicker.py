import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
try:
    import pyautogui
except ImportError:
    pyautogui = None

class AutoClicker:
    def __init__(self, master):
        self.master = master
        master.title("Auto Clicker")

        self.duration_var = tk.DoubleVar(value=5.0)
        self.frequency_var = tk.DoubleVar(value=1.0)
        self.running = False
        self.thread = None

        ttk.Label(master, text="Duration (seconds):").grid(column=0, row=0, padx=5, pady=5, sticky="w")
        ttk.Entry(master, textvariable=self.duration_var, width=10).grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(master, text="Clicks per second:").grid(column=0, row=1, padx=5, pady=5, sticky="w")
        ttk.Entry(master, textvariable=self.frequency_var, width=10).grid(column=1, row=1, padx=5, pady=5)

        self.start_button = ttk.Button(master, text="Start", command=self.start_clicking)
        self.start_button.grid(column=0, row=2, padx=5, pady=5, columnspan=2, sticky="we")

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_clicking, state="disabled")
        self.stop_button.grid(column=0, row=3, padx=5, pady=5, columnspan=2, sticky="we")

        ttk.Label(master, text="Note: Requires pyautogui module").grid(column=0, row=4, columnspan=2)

    def _click_loop(self, duration, interval):
        start_time = time.time()
        while self.running and (time.time() - start_time < duration):
            if pyautogui:
                pyautogui.click()
            time.sleep(interval)
        self.stop_clicking()

    def start_clicking(self):
        if not pyautogui:
            messagebox.showerror("Error", "pyautogui module not installed")
            return
        if self.running:
            return
        duration = max(0.0, self.duration_var.get())
        frequency = max(0.1, self.frequency_var.get())
        interval = 1.0 / frequency
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.thread = threading.Thread(target=self._click_loop, args=(duration, interval), daemon=True)
        self.thread.start()

    def stop_clicking(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")


def main():
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
