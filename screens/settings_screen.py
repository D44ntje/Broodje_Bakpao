import customtkinter as ctk
from PIL import Image
from login import fetch_user_info

class SettingsScreen:
    def __init__(self, parent, steam_id, logout_callback):
        self.parent = parent
        self.steam_id = steam_id
        self.logout_callback = logout_callback

        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(parent, fg_color="#171A21")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        section_frame = ctk.CTkFrame(self.main_frame, fg_color="#1B2838", corner_radius=10)
        section_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        section_frame.grid_rowconfigure(0, weight=1)
        section_frame.grid_columnconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        user_info = self.get_user_information()

        ctk.CTkLabel(content_frame, text="User Information", font=("Arial", 25), text_color="white").pack(pady=10)

        username_text = user_info.get('username', 'No username available')
        steam_id_text = user_info.get('steam_id', 'No Steam ID available')

        ctk.CTkLabel(content_frame, text=f"Username: {username_text}", font=("Arial", 14), text_color="white").pack(pady=5)
        ctk.CTkLabel(content_frame, text=f"Steam ID: {steam_id_text}", font=("Arial", 14), text_color="white").pack(pady=5)

        ctk.CTkLabel(content_frame, text="Thank you for using our platform!\nFeel free to donate any amount at any time.",
                     font=("Arial", 14), text_color="white").pack(pady=10)

        # Try loading the Tikkie donation QR code image
        tikkie_code = "icons/support_tikkie.png"
        try:
            image = Image.open(tikkie_code)
            tikkie_image = ctk.CTkImage(light_image=image, dark_image=image, size=(250, 250))
            image_label = ctk.CTkLabel(content_frame, image=tikkie_image, text="")
            image_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")

    def get_user_information(self):
        try:
            if self.steam_id:
                user_info = fetch_user_info(self.steam_id)
                if user_info:
                    return user_info
            return {}
        except Exception as e:
            print(f"Error fetching user information: {e}")
            return {}

    def clear_parent(self):
        for widget in self.parent.winfo_children():
            widget.destroy()