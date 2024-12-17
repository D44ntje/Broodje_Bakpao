import customtkinter as ctk

class HomeScreen:
    def __init__(self, parent):
        ctk.CTkLabel(parent, text="Home Screen", font=("Arial", 24), text_color="white").pack(pady=20)
