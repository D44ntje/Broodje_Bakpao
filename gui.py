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

        self.frame = tk.Frame(self.root, bg="#171A21")
        self.frame.pack(expand=True)

        label = tk.Label(self.frame, text="Welcome to Steam", bg="#171A21", fg="#FFFFFF", font=("Arial", 36, "bold"))
        label.pack(pady=20)

        start_button = ttk.Button(self.frame, text="Start", style="TButton", command=self.show_next_screen)
        start_button.pack(pady=10)

        exit_button = ttk.Button(self.frame, text="Exit", style="TButton", command=self.root.destroy)
        exit_button.pack(pady=10)

    def show_next_screen(self):
        # Clear the existing frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Add new content to the frame
        next_label = tk.Label(self.frame, text="This is the next screen", bg="#171A21", fg="#FFFFFF", font=("Arial", 36, "bold"))
        next_label.pack(pady=20)

        back_button = ttk.Button(self.frame, text="Back", style="TButton", command=self.show_main_screen)
        back_button.pack(pady=10)

    def show_main_screen(self):
        # Clear the current frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Recreate the main screen content
        label = tk.Label(self.frame, text="Welcome to Steam", bg="#171A21", fg="#FFFFFF", font=("Arial", 36, "bold"))
        label.pack(pady=20)

        start_button = ttk.Button(self.frame, text="Start", style="TButton", command=self.show_next_screen)
        start_button.pack(pady=10)

        exit_button = ttk.Button(self.frame, text="Exit", style="TButton", command=self.root.destroy)
        exit_button.pack(pady=10)

    def run(self):
        self.root.mainloop()

    def run(self):
        self.root.mainloop()
