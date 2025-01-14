import customtkinter as ctk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os

class FriendsScreen:
    def __init__(self, parent, steam_id):
        self.parent = parent
        self.steam_id = steam_id
        self.create_ui()

    def create_ui(self):
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self.parent, fg_color="#171A21")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        section_frame = ctk.CTkFrame(self.main_frame, fg_color="#1B2838", corner_radius=10)
        section_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.header_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        self.header_frame.pack(pady=10, fill="x", padx=10)

        self.header_label = ctk.CTkLabel(self.header_frame, text="Friends List", font=("Arial", 25), text_color="white")
        self.header_label.pack(side="left")

        self.friends_count_label = ctk.CTkLabel(self.header_frame, text="", font=("Arial", 18), text_color="gray")
        self.friends_count_label.pack(side="left", padx=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(section_frame, width=600, height=400, fg_color="#171A21", corner_radius=10)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_friends_list()

    def load_friends_list(self):
        friends_url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={os.getenv('STEAM_API_KEY')}&steamid={self.steam_id}&relationship=friend"
        response = requests.get(friends_url)

        if response.status_code == 200:
            friends_data = response.json().get('friendslist', {}).get('friends', [])
            if not friends_data:
                ctk.CTkLabel(self.scrollable_frame, text="No friends found.", font=("Arial", 14), text_color="white").pack(pady=10)
                return

            self.friends_count_label.configure(text=f"({len(friends_data)} total)")

            for friend in friends_data:
                friend_info = self.fetch_friend_info(friend['steamid'])
                if friend_info:
                    self.add_friend_row(friend_info)
        else:
            ctk.CTkLabel(self.scrollable_frame, text="Failed to fetch friends list.", font=("Arial", 14), text_color="white").pack(pady=10)

    def fetch_friend_info(self, friend_steam_id):
        user_info_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={os.getenv('STEAM_API_KEY')}&steamids={friend_steam_id}"
        response = requests.get(user_info_url)

        if response.status_code == 200:
            players = response.json().get('response', {}).get('players', [])
            if players:
                return players[0]
        return None

    def add_friend_row(self, friend_info):
        avatar_url = friend_info['avatar']
        username = friend_info['personaname']
        status = "Online" if friend_info['personastate'] == 1 else "Offline"

        avatar_image = self.download_avatar(avatar_url)

        friend_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1B2838", corner_radius=10)
        friend_frame.pack(padx=10, pady=10, fill="x", expand=True)

        if avatar_image:
            avatar_label = ctk.CTkLabel(friend_frame, image=avatar_image, text="")
            avatar_label.image = avatar_image
            avatar_label.pack(side="left", padx=10)

        details_frame = ctk.CTkFrame(friend_frame, fg_color="transparent")
        details_frame.pack(side="left", padx=10, fill="both", expand=True)

        username_label = ctk.CTkLabel(details_frame, text=username, font=("Arial", 16, "bold"), text_color="white")
        username_label.pack(anchor="w")

        status_label = ctk.CTkLabel(details_frame, text=f"Status: {status}", font=("Arial", 14),
                                    text_color="green" if status == "Online" else "red")
        status_label.pack(anchor="w")

    def download_avatar(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = Image.open(BytesIO(response.content)).resize((40, 40))
            return ctk.CTkImage(light_image=image_data, size=(40, 40))
        except requests.RequestException as e:
            print(f"Error downloading avatar: {e}")
            return None

    def clear_parent(self):
        for widget in self.parent.winfo_children():
            widget.destroy()