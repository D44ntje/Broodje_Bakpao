import customtkinter as ctk
from PIL import Image
from login import get_user_info

class SettingsScreen:
    def __init__(self, parent, logout_callback):
        self.parent = parent
        self.logout_callback = logout_callback
        self.clear_parent()
        self.main_label = ctk.CTkLabel(parent, text="Settings Screen", font=("Arial", 24), text_color="white")
        self.main_label.pack(pady=20)
        center_frame = ctk.CTkFrame(parent, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        user_info = self.get_user_information()
        self.label_user = ctk.CTkLabel(center_frame, text="This is your user information:", text_color="white")
        self.label_user.pack(pady=10)
        username_text = user_info.get('username', 'No username available')
        self.label1 = ctk.CTkLabel(center_frame, text=f"Username: {username_text}", text_color="white")
        self.label1.pack(pady=5)
        steam_id_text = user_info.get('steam_id', 'No Steam ID available')
        self.label2 = ctk.CTkLabel(center_frame, text=f"Steam ID: {steam_id_text}", text_color="white")
        self.label2.pack(pady=5)
        self.label3 = ctk.CTkLabel(center_frame, text="Thank you for using us!\nFeel free to donate any amount at any time.", text_color="white")
        self.label3.pack(pady=10)
        tikkie_code = "icons/support_tikkie.png"
        try:
            image = Image.open(tikkie_code)
            tikkie_image = ctk.CTkImage(light_image=image, dark_image=image, size=(250, 250))
            image_label = ctk.CTkLabel(center_frame, image=tikkie_image, text="")
            image_label.pack(side="bottom", pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")
        self.logout_button = ctk.CTkButton(parent, text="Log Out", command=self.logout)
        self.logout_button.place(relx=0.5, rely=0.95, anchor="center")

    def get_user_information(self):
        try:
            user_info = get_user_info()
            if user_info:
                return user_info
            return {}
        except Exception as e:
            print(f"Error fetching user information: {e}")
            return {}

    def clear_parent(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def logout(self):
        if self.logout_callback:
            self.logout_callback()
