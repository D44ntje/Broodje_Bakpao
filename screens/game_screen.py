import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import webbrowser

class GameScreen:
    def __init__(self, parent):
        self.parent = parent

        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(parent, fg_color="#171A21")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        section_frame = ctk.CTkFrame(self.main_frame, fg_color="#1B2838", corner_radius=10)
        section_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.scrollable_frame = ctk.CTkScrollableFrame(section_frame, width=800, height=600, fg_color="transparent")
        self.scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

        all_games_data, b0, b1 = self.generate_graph()
        self.most_popular_games, self.most_expensive_games = self.get_top_games()

        self.add_top_games_segment(self.scrollable_frame, "Top 5 worldwide", self.most_popular_games)
        self.add_top_games_segment(self.scrollable_frame, "Top 5 most expensive", self.most_expensive_games)
        self.display_graph(self.scrollable_frame)

    def generate_graph(self):
        """
        Generates a graph based on game data and saves it as an image.
        """
        json_file_path = os.path.join(os.path.dirname(__file__), "../steam.json")

        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        names, owners, prices, all_games_data = [], [], [], []

        for item in data:
            price = item.get('price')
            if price is not None:
                current_price = float(price)
                all_games_data.append((item['name'], item['owners'], price))
                if current_price <= 400:
                    names.append(item['name'])
                    owners.append(item['owners'])
                    prices.append(price)

        def mean(values):
            return sum(values) / len(values)

        def linear_regression(X, y):
            n = len(X)
            x_mean = mean(X)
            y_mean = mean(y)
            numerator = sum((X[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            denominator = sum((X[i] - x_mean) ** 2 for i in range(n))
            if denominator == 0:
                raise ValueError("Denominator in linear regression calculation is zero. Check for variation in the data.")
            b1 = numerator / denominator
            b0 = y_mean - b1 * x_mean
            return b0, b1

        X = [int(owner.split(' - ')[0]) if ' - ' in owner else int(owner.replace(',', '')) for owner in owners]
        y = [float(price) for price in prices]

        try:
            b0, b1 = linear_regression(X, y)
        except ValueError as e:
            print(e)
            exit()

        predictions = [b0 + b1 * int(owner.split(' - ')[0]) if ' - ' in owner else b0 + b1 * int(owner.replace(',', '')) for owner in owners]

        plt.figure(figsize=(13, 5))
        plt.scatter(X, y, color='blue', label='Actual Prices', s=30)
        plt.plot(X, predictions, color='red', label='Predicted Prices', linewidth=1.5)
        plt.title('Predicted Prices Based on Number of Owners')
        plt.xlabel('Number of Owners')
        plt.ylabel('Prices')
        plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, nbins=12))
        plt.legend()
        plt.grid()

        plt.figtext(0.5, -0.15,
                    "This graph indicates the coherence between the amount of players in each game and the price of the game. "
                    "The blue dots indicate each game in the Steam store, and the red line indicates the AI prediction of what the price should be based on the amount of players playing a game.",
                    wrap=True, horizontalalignment='center', fontsize=10, fontweight='bold')

        plt.savefig('predicted_prices_plot.png', format='png', bbox_inches='tight')
        plt.close()

        return all_games_data, b0, b1

    def get_top_games(self):
        """
        Returns the predefined top 5 most popular and most expensive games.
        """
        most_popular_games = [
            ("Dota 2", "NA", "Free", 0),
            ("New World Aeternum", "NA", "$39.99", 0),
            ("PUBG BATTLEGROUNDS", "NA", "$29.99", 0),
            ("Team Fortress 2", "NA", "Free", 0),
            ("Counter-Strike", "NA", "$9.99", 0)
        ]

        most_expensive_games = [
            ("The Leverage Game", "NA", "$1,000.00", 0),
            ("The Leverage Game: Business Edition", "NA", "$1,200.00", 0),
            ("Ascent Free-Roaming VR Experience", "NA", "$999.00", 0),
            ("Aartform Curvy 3D 3.0", "NA", "$599.00", 0),
            ("Houdini Indie", "NA", "$399.00", 0)
        ]

        return most_popular_games, most_expensive_games

    def add_expanding_segment(self, parent, title, description, row):
        segment_frame = ctk.CTkFrame(parent, fg_color="#1B2838", corner_radius=10)
        segment_frame.grid(row=row, column=0, padx=20, pady=20, sticky="nsew")

        title_label = ctk.CTkLabel(segment_frame, text=title, font=("Arial", 18), text_color="white")
        title_label.pack(anchor="w", padx=10)

        description_label = ctk.CTkLabel(segment_frame, text=description, font=("Arial", 12), text_color="white")
        description_label.pack(anchor="w", padx=10)

    def add_top_games_segment(self, parent, title, games):
        segment_frame = ctk.CTkFrame(parent, fg_color="#1B2838", corner_radius=10)
        segment_frame.pack(pady=10, padx=10, fill="x")

        title_label = ctk.CTkLabel(segment_frame, text=title, font=("Arial", 18), text_color="white")
        title_label.pack(anchor="w", padx=10)

        urls = {
            "Dota 2": "https://store.steampowered.com/app/570/Dota_2/",
            "New World Aeternum": "https://store.steampowered.com/app/1063730/New_World_Aeternum/",
            "PUBG BATTLEGROUNDS": "https://store.steampowered.com/app/578080/PUBG_BATTLEGROUNDS/",
            "Team Fortress 2": "https://store.steampowered.com/app/440/Team_Fortress_2/",
            "Counter-Strike": "https://store.steampowered.com/app/10/CounterStrike/",
            "The Leverage Game": "https://store.steampowered.com/app/2499620/The_Leverage_Game/",
            "The Leverage Game: Business Edition": "https://store.steampowered.com/app/2504210/The_Leverage_Game_Business_Edition/",
            "Ascent Free-Roaming VR Experience": "https://store.steampowered.com/app/1200520/Ascent_FreeRoaming_VR_Experience/",
            "Aartform Curvy 3D 3.0": "https://store.steampowered.com/app/253670/Aartform_Curvy_3D_30/",
            "Houdini Indie": "https://store.steampowered.com/app/502570/Houdini_Indie/"
        }

        for game in games:
            row_frame = ctk.CTkFrame(segment_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)

            game_label = ctk.CTkLabel(row_frame,
                                      text=f"{game[0]} (Owners: {game[1]}, Price: {game[2]}, Predicted: {game[3]:.2f})",
                                      font=("Arial", 12), text_color="white")
            game_label.pack(side="left", padx=10)

            info_button = ctk.CTkButton(
                row_frame,
                text="Click for more information!",
                width=200,
                command=lambda url=urls.get(game[0], "#"): webbrowser.open(url)
            )
            info_button.pack(side="right", padx=10)

    def display_graph(self, parent):
        """
        Loads and displays the saved graph image.
        """
        graph_image = Image.open('predicted_prices_plot.png')
        graph_photo = ImageTk.PhotoImage(graph_image)

        graph_frame = ctk.CTkFrame(parent, fg_color="transparent")
        graph_frame.pack(pady=10, padx=10, fill="x")

        graph_label = ctk.CTkLabel(graph_frame, image=graph_photo, text="")
        graph_label.image = graph_photo
        graph_label.pack()
