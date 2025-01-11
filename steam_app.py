import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from login import open_steam_login, start_flask, set_login_callback, get_rfid_user_info, log_user_login
import threading
from screens.admin_dashboard_screen import AdminDashboardScreen
from helpers.databasehelper import DatabaseHelper
from screens.game_screen import GameScreen
from screens.home_screen import HomeScreen
from screens.friends_screen import FriendsScreen
from screens.settings_screen import SettingsScreen

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class SteamApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Steam GUI")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        self.db_config = {
            "host": "108.143.125.97",
            "database": "SteamDatabase",
            "user": "postgres",
            "password": "1GratjeMooiBeest"
        }
        self.db_helper = DatabaseHelper(self.db_config)

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
        """
        Display the main login screen.
        """
        self.clear_content()

        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.grid(row=1, column=0, sticky="nsew", pady=20)

        welcome_label = ctk.CTkLabel(button_frame, text="Welcome to Steam", font=("Arial", 36, "bold"),
                                     text_color="white")
        welcome_label.pack(pady=20)

        login_button = ctk.CTkButton(button_frame, text="Login with Steam", command=self.login, height=40, width=200)
        login_button.pack(pady=10)

        login_rfid_button = ctk.CTkButton(button_frame, text="Login with RFID", command=self.login_rfid, height=40,
                                          width=200)
        login_rfid_button.pack(pady=10)

        admin_button = ctk.CTkButton(button_frame, text="Admin Panel", command=self.show_admin_login, height=40,
                                     width=200)
        admin_button.pack(pady=10)

        exit_button = ctk.CTkButton(button_frame, text="Exit", command=self.root.destroy, height=40, width=200)
        exit_button.pack(pady=10)

    def login(self):
        open_steam_login()

    def login_rfid(self):
        """
        Attempt to login using the last successful RFID login attempt.
        """
        user_info = get_rfid_user_info()
        if user_info:
            log_user_login(user_info)
            self.show_dashboard(user_info)
        else:
            self.display_error_message("Failed to retrieve RFID login or user info.")

    def display_error_message(self, message):
        self.clear_content()
        error_label = ctk.CTkLabel(self.content_frame, text=message, font=("Arial", 14), text_color="red")
        error_label.pack(pady=10)

    def show_dashboard(self, user_info):
        """
        Displays the main dashboard after Steam login.
        """
        username = user_info["username"]
        avatar_url = user_info["avatar_url"]

        self.clear_content()
        self.create_sidebar(username, avatar_url)

        HomeScreen(self.content_frame)

    def create_sidebar(self, username, avatar_url):
        if self.sidebar:
            self.sidebar.destroy()

        self.sidebar = ctk.CTkFrame(self.root, fg_color="#1B2838", width=300)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        avatar_image = self.download_avatar(avatar_url)
        if avatar_image:
            avatar_label = ctk.CTkLabel(self.sidebar, image=avatar_image, text="")
            avatar_label.image = avatar_image
            avatar_label.pack(pady=20)

        username_label = ctk.CTkLabel(self.sidebar, text=username, font=("Arial", 20), text_color="white")
        username_label.pack(pady=10)

        self.add_navigation_button("Home", lambda: self.populate_content("home"))
        self.add_navigation_button("Friends", lambda: self.populate_content("friends"))
        self.add_navigation_button("Games", lambda: self.populate_content("games"))
        self.add_navigation_button("Settings", lambda: self.populate_content("settings"))

        logout_button = ctk.CTkButton(self.sidebar, text="Log Out", command=self.logout, height=40, width=200)
        logout_button.pack(side="bottom", pady=20)

    def add_navigation_button(self, label, command):
        button = ctk.CTkButton(
            self.sidebar,
            text=label,
            font=("Arial", 14),
            fg_color="transparent",
            hover_color="#2A475E",
            command=command
        )
        button.pack(pady=10)

    def show_admin_login(self):
        self.clear_content()

        login_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        login_frame.grid(row=1, column=0, sticky="nsew")

        admin_label = ctk.CTkLabel(login_frame, text="Admin Panel Login", font=("Arial", 28, "bold"), text_color="white")
        admin_label.pack(pady=20)

        username_label = ctk.CTkLabel(login_frame, text="Username:", font=("Arial", 16), text_color="white")
        username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(login_frame, width=250, height=35)
        self.username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(login_frame, text="Password:", font=("Arial", 16), text_color="white")
        password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(login_frame, width=250, height=35, show="*")
        self.password_entry.pack(pady=5)

        login_button = ctk.CTkButton(login_frame, text="Login", command=self.admin_login_attempt, height=40, width=200)
        login_button.pack(pady=10)

        back_button = ctk.CTkButton(login_frame, text="Back", command=self.show_main_screen, height=40, width=200)
        back_button.pack(pady=10)

    def admin_login_attempt(self):
        """
        Verify admin credentials and show the admin dashboard if valid.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        with self.db_helper.connect() as cursor:
            cursor.execute("SELECT * FROM admin_users WHERE username = %s AND password = %s", (username, password))
            if cursor.fetchone():
                self.clear_content()
                AdminDashboardScreen(self.content_frame, self.db_helper)
            else:
                self.display_error_message("Invalid credentials! Please try again.")

    def populate_content(self, screen_name):
        self.clear_content()
        if screen_name == "home":
            HomeScreen(self.content_frame)
        elif screen_name == "friends":
            FriendsScreen(self.content_frame)
        elif screen_name == "games":
            GameScreen(self.content_frame)
        elif screen_name == "settings":
            SettingsScreen(self.content_frame, self.logout)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def download_avatar(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = Image.open(BytesIO(response.content)).resize((150, 150))
            return ctk.CTkImage(light_image=image_data, size=(150, 150))
        except requests.RequestException:
            return None

    def logout(self):
        if self.sidebar:
            self.sidebar.destroy()
            self.sidebar = None
        self.show_main_screen()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SteamApp()
    app.run()