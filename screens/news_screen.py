import customtkinter as ctk

class NewsScreen:
    def __init__(self, parent):
        ctk.CTkLabel(parent, text="News Screen", font=("Arial", 24), text_color="white").pack(pady=20)
