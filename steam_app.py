import customtkinter as ctk
import threading
from login import open_steam_login, start_flask, set_login_callback, get_user_info
from utils.avatar_utils import download_avatar
from utils.navigation_utils import add_navigation_button
from screens.home_screen import HomeScreen
from screens.friends_screen import FriendsScreen
from screens.news_screen import NewsScreen
from screens.settings_screen import SettingsScreen

class SteamApp:
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title("Steam GUI")
        self.root.attributes("-fullscreen", True)

        # Sidebar
        self.sidebar = None
        self.content_frame = ctk.CTkFrame(self.root, fg_color="#171A21")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.show_main_screen()

        flask_thread = threading.Thread(target=start_flask, daemon=True)
        flask_thread.start()
        set_login_callback(self.show_dashboard)

    def show_main_screen(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Welcome to Steam", font=("Arial", 36, "bold"), text_color="white").pack(pady=20)
        ctk.CTkButton(self.content_frame, text="Login with Steam", command=self.login).pack(pady=10)
        ctk.CTkButton(self.content_frame, text="Exit", command=self.root.destroy).pack(pady=10)

    def login(self):
        open_steam_login()

    def show_dashboard(self, steam_id):
        user_info = get_user_info()
        if user_info:
            self.create_sidebar(user_info["username"], user_info["avatar_url"])
            self.show_screen("home")

    def create_sidebar(self, username, avatar_url):
        if self.sidebar:
            self.sidebar.destroy()

        self.sidebar = ctk.CTkFrame(self.root, fg_color="#1B2838", width=300)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Avatar and username
        avatar_image = download_avatar(avatar_url)
        ctk.CTkLabel(self.sidebar, image=avatar_image, text="").pack(pady=20)
        ctk.CTkLabel(self.sidebar, text=username, font=("Arial", 20), text_color="white").pack(pady=10)

        # Navigation Buttons
        add_navigation_button(self.sidebar, "Home", "icons/home.png", lambda: self.show_screen("home"))
        add_navigation_button(self.sidebar, "Friends", "icons/friends.png", lambda: self.show_screen("friends"))
        add_navigation_button(self.sidebar, "News", "icons/news.png", lambda: self.show_screen("news"))
        add_navigation_button(self.sidebar, "Settings", "icons/settings.png", lambda: self.show_screen("settings"))


    def show_screen(self, screen_name):
        self.clear_content()
        if screen_name == "home":
            HomeScreen(self.content_frame)
        elif screen_name == "friends":
            FriendsScreen(self.content_frame)
        elif screen_name == "news":
            NewsScreen(self.content_frame)
        elif screen_name == "settings":
            SettingsScreen(self.content_frame, self.logout)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def logout(self):
        self.sidebar.destroy()
        self.sidebar = None
        self.show_main_screen()

    def run(self):
        self.root.mainloop()
