import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from login import open_steam_login, start_flask, set_login_callback, get_user_info
import threading

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

        login_button = ttk.Button(self.frame, text="Login with Steam", style="TButton", command=self.login)
        login_button.pack(pady=10)

        exit_button = ttk.Button(self.frame, text="Exit", style="TButton", command=self.root.destroy)
        exit_button.pack(pady=10)

        # Start Flask server
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.daemon = True
        flask_thread.start()

        # Set the login callback to display the dashboard after login
        set_login_callback(self.show_dashboard)

    def login(self):
        """
        Initiates Steam login process.
        """
        open_steam_login()

    def show_dashboard(self, steam_id):
        """
        Displays the dashboard screen with the user's avatar, username, and Steam ID.
        """
        # Get the user info (username, Steam ID, and avatar URL)
        user_info = get_user_info()
        if user_info:
            username = user_info["username"]
            steam_id = user_info["steam_id"]
            avatar_url = user_info["avatar_url"]

            # Clear the current frame
            for widget in self.frame.winfo_children():
                widget.destroy()

            # Download and display avatar image
            avatar_image = self.download_avatar(avatar_url)
            if avatar_image:
                avatar_label = tk.Label(self.frame, image=avatar_image, bg="#171A21")
                avatar_label.image = avatar_image  # Keep a reference to avoid garbage collection
                avatar_label.pack(pady=10)

            # Display username
            username_label = tk.Label(self.frame, text=f"Username: {username}", bg="#171A21", fg="#FFFFFF", font=("Arial", 24))
            username_label.pack(pady=10)

            # Display Steam ID
            steam_id_label = tk.Label(self.frame, text=f"Steam ID: {steam_id}", bg="#171A21", fg="#FFFFFF", font=("Arial", 24))
            steam_id_label.pack(pady=10)

            back_button = ttk.Button(self.frame, text="Log Out", style="TButton", command=self.show_main_screen)
            back_button.pack(pady=10)

    def download_avatar(self, url):
        """
        Downloads the avatar image from the URL and converts it to a format compatible with Tkinter.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = Image.open(BytesIO(response.content))
            return ImageTk.PhotoImage(image_data)
        except requests.RequestException as e:
            print(f"Error downloading avatar image: {e}")
            return None

    def show_main_screen(self):
        """
        Returns to the main screen.
        """
        for widget in self.frame.winfo_children():
            widget.destroy()

        label = tk.Label(self.frame, text="Welcome to Steam", bg="#171A21", fg="#FFFFFF", font=("Arial", 36, "bold"))
        label.pack(pady=20)

        login_button = ttk.Button(self.frame, text="Login with Steam", style="TButton", command=self.login)
        login_button.pack(pady=10)

        exit_button = ttk.Button(self.frame, text="Exit", style="TButton", command=self.root.destroy)
        exit_button.pack(pady=10)

    def run(self):
        self.root.mainloop()
