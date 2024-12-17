import customtkinter as ctk
from PIL import Image

def add_navigation_button(parent, label, icon_path, command):
    try:
        icon = Image.open(icon_path).resize((20, 20))
        icon_image = ctk.CTkImage(light_image=icon, size=(20, 20))

        button = ctk.CTkButton(
            parent,
            text=label,
            image=icon_image,
            compound="top",
            font=("Arial", 14),
            fg_color="transparent",
            hover_color="#2A475E",
            command=command
        )
        button.image = icon_image  # Prevent garbage collection
        button.pack(pady=10)
    except Exception as e:
        print(f"Error loading navigation icon '{icon_path}': {e}")
