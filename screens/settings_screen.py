import customtkinter as ctk

class SettingsScreen:
    def __init__(self, parent):
        ctk.CTkLabel(parent, text="Settings Screen", font=("Arial", 24), text_color="white").pack(pady=20)
