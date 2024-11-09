import tkinter as tk
from tkinter import ttk

class SteamApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Steam GUI")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#171A21")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        background="#1B2838",
                        foreground="#C5C3C0",
                        font=("Arial", 20, "bold"),
                        borderwidth=0,
                        focuscolor="none")

        style.map("TButton",
                  background=[("active", "#2A475E")],
                  foreground=[("active", "#FFFFFF")])

        frame = tk.Frame(self.root, bg="#171A21")
        frame.pack(expand=True)

        label = tk.Label(frame, text="Welcome to Steam", bg="#171A21", fg="#FFFFFF", font=("Arial", 36, "bold"))
        label.pack(pady=20)

        button = ttk.Button(frame, text="Start", style="TButton")
        button.pack(pady=10)

        exit_button = ttk.Button(frame, text="Exit", style="TButton", command=self.root.destroy)
        exit_button.pack(pady=10)

    def run(self):
        self.root.mainloop()
