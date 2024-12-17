import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from login import open_steam_login, start_flask, set_login_callback, get_user_info
import threading

# CustomTkinter appearance settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class SteamApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Steam GUI")
        self.root.attributes("-fullscreen", True)

        # Sidebar
        self.sidebar = None

        # Main Content Frame
        self.content_frame = ctk.CTkFrame(self.root, fg_color="#171A21")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.show_main_screen()

        # Start Flask server
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.daemon = True
        flask_thread.start()

        # Set the login callback
        set_login_callback(self.show_dashboard)

    def show_main_screen(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(self.content_frame, text="Welcome to Steam", font=("Arial", 36, "bold"), text_color="white")
        label.pack(pady=20)

        login_button = ctk.CTkButton(self.content_frame, text="Login with Steam", command=self.login, height=40, width=200)
        login_button.pack(pady=10)

        exit_button = ctk.CTkButton(self.content_frame, text="Exit", command=self.root.destroy, height=40, width=200)
        exit_button.pack(pady=10)

    def login(self):
        open_steam_login()

    def show_dashboard(self, steam_id):
        user_info = get_user_info()
        if user_info:
            username = user_info["username"]
            avatar_url = user_info["avatar_url"]

            for widget in self.content_frame.winfo_children():
                widget.destroy()

            self.create_sidebar(username, avatar_url)
            self.populate_main_content()

    def create_sidebar(self, username, avatar_url):
        if self.sidebar:
            self.sidebar.destroy()

        self.sidebar = ctk.CTkFrame(self.root, fg_color="#1B2838", width=300)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Avatar
        avatar_image = self.download_avatar(avatar_url)
        if avatar_image:
            avatar_label = ctk.CTkLabel(self.sidebar, image=avatar_image, text="")
            avatar_label.image = avatar_image
            avatar_label.pack(pady=20)

        # Username
        username_label = ctk.CTkLabel(self.sidebar, text=username, font=("Arial", 20), text_color="white")
        username_label.pack(pady=10)

        # Navigation Buttons with Icons
        self.add_navigation_item("Home", "icons/home.png", self.on_home_click)
        self.add_navigation_item("Friends", "icons/friends.png", self.on_friends_click)
        self.add_navigation_item("News", "icons/news.png", self.on_news_click)
        self.add_navigation_item("Settings", "icons/settings.png", self.on_settings_click)

        # Logout Button
        logout_button = ctk.CTkButton(self.sidebar, text="Log Out", command=self.logout, height=40, width=200)
        logout_button.pack(side="bottom", pady=20)

    def add_navigation_item(self, label, icon_path, command):
        """
        Adds a navigation button with an icon and text to the sidebar.
        """
        try:
            # Load the icon image
            icon = Image.open(icon_path).resize((20, 20))  # Resize the icon
            icon_image = ctk.CTkImage(light_image=icon, size=(20, 20))

            # Navigation button
            nav_button = ctk.CTkButton(
                self.sidebar,
                image=icon_image,
                text=label,
                compound="top",  # Icon above the text
                font=("Arial", 14),
                height=80,
                width=200,
                fg_color="transparent",  # Transparent background
                hover_color="#2A475E",   # Hover effect color
                command=command
            )
            nav_button.image = icon_image  # Prevent garbage collection
            nav_button.pack(pady=10)
        except Exception as e:
            print(f"Error loading icon '{icon_path}': {e}")

    def on_home_click(self):
        """
        Function to handle Home button click.
        """
        self.populate_content("Home Screen")

    def on_friends_click(self):
        """
        Function to handle Friends button click.
        """
        self.populate_content("Friends Screen")

    def on_news_click(self):
        """
        Function to handle News button click.
        """
        self.populate_content("News Screen")

    def on_settings_click(self):
        """
        Function to handle Settings button click.
        """
        self.populate_content("Settings Screen")

    def populate_content(self, screen_name):
        """
        Updates the main content area with the selected screen.
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        content_label = ctk.CTkLabel(self.content_frame, text=screen_name, font=("Arial", 24), text_color="white")
        content_label.pack(pady=20)

    def populate_main_content(self):
        """
        Default dashboard content.
        """
        self.populate_content("Dashboard Content")

    def download_avatar(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = Image.open(BytesIO(response.content)).resize((150, 150))
            return ctk.CTkImage(light_image=image_data, size=(150, 150))
        except requests.RequestException as e:
            print(f"Error downloading avatar image: {e}")
            return None

    def logout(self):
        global steam_id
        steam_id = None

        if self.sidebar:
            self.sidebar.destroy()
            self.sidebar = None

        self.show_main_screen()

    def run(self):
        self.root.mainloop()

# Run the app
if __name__ == "__main__":
    app = SteamApp()
    app.run()
