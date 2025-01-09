import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import customtkinter as ctk
from PIL import Image, ImageTk

# Function to generate the graph and save it as an image
def generate_graph():
    json_file_path = r'C:\Users\Gebruiker\OneDrive - ASG\Documenten\HU\steam.json'

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    names = []
    owners = []
    prices = []
    all_games_data = []

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

    X = []
    for owner in owners:
        if ' - ' in owner:
            lower_bound = int(owner.split(' - ')[0])
            X.append(lower_bound)
        else:
            X.append(int(owner.replace(',', '')))

    y = [float(price) for price in prices]

    try:
        b0, b1 = linear_regression(X, y)
    except ValueError as e:
        print(e)
        exit()

    def predict(x):
        return b0 + b1 * x

    predictions = []
    for owner in owners:
        if ' - ' in owner:
            lower_bound = int(owner.split(' - ')[0])
            predictions.append(predict(lower_bound))
        else:
            predictions.append(predict(int(owner.replace(',', ''))))

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

    plt.figtext(0.5, -0.1,
                "This graph indicates the coherence between the amount of players in each game and the price of the game. "
                "The blue dots indicate each game in the Steam store, and the red line indicates the AI prediction of what the price should be based on the amount of players playing a game.",
                wrap=True, horizontalalignment='center', fontsize=10, fontweight='bold')

    plt.savefig('predicted_prices_plot.png', format='png', bbox_inches='tight')
    plt.close()

    return all_games_data, b0, b1

# Function to get the top 5 most popular and most expensive games
def get_top_games(all_games_data, b0, b1):
    def predict(x):
        return b0 + b1 * x

    games_data = []
    for name, owners, price in all_games_data:
        if ' - ' in owners:
            lower_bound = int(owners.split(' - ')[0])
        else:
            lower_bound = int(owners.replace(',', ''))
        predicted_price = predict(lower_bound)
        games_data.append((name, owners, price, predicted_price))

    most_popular_games = sorted(games_data, key=lambda x: int(x[1].split(' - ')[0]) if ' - ' in x[1] else int(x[1].replace(',', '')), reverse=True)[:5]
    most_expensive_games = sorted(games_data, key=lambda x: float(x[2]), reverse=True)[:5]

    return most_popular_games, most_expensive_games

class GameScreen:
    def __init__(self, parent):
        ctk.CTkLabel(parent, text="Game Screen", font=("Arial", 24), text_color="white").pack(pady=20)

        self.search_bar = ctk.CTkEntry(parent, placeholder_text="Search for a game...")
        self.search_bar.pack(pady=(0, 20), padx=10, fill="x")

        self.add_expanding_segment(parent, "Recommended by friends", "This section shows games recommended by your friends.")

        # Generate graph and top games data
        all_games_data, b0, b1 = generate_graph()
        self.most_popular_games, self.most_expensive_games = get_top_games(all_games_data, b0, b1)

        self.add_top_games_segment(parent, "Top 5 worldwide", self.most_popular_games)

        # Display the graph
        self.display_graph(parent)

    def add_expanding_segment(self, parent, title, description):
        segment_frame = ctk.CTkFrame(parent)
        segment_frame.pack(pady=10, padx=10, fill="x")

        title_label = ctk.CTkLabel(segment_frame, text=title, font=("Arial", 18), text_color="white")
        title_label.pack(anchor="w", padx=10)

        description_label = ctk.CTkLabel(segment_frame, text=description, font=("Arial", 12), text_color="white")
        description_label.pack(anchor="w", padx=10)

    def add_top_games_segment(self, parent, title, games):
        segment_frame = ctk.CTkFrame(parent)
        segment_frame.pack(pady=10, padx=10, fill="x")

        title_label = ctk.CTkLabel(segment_frame, text=title, font=("Arial", 18), text_color="white")
        title_label.pack(anchor="w", padx=10)

        for game in games:
            game_label = ctk.CTkLabel(segment_frame, text=f"{game[0]} (Owners: {game[1]}, Price: {game[2]}, Predicted: {game[3]:.2f})", font=("Arial", 12), text_color="white")
            game_label.pack(anchor="w", padx=10)

    def display_graph(self, parent):
        # Load the saved graph image
        graph_image = Image.open('predicted_prices_plot.png')
        graph_photo = ImageTk.PhotoImage(graph_image)

        graph_label = ctk.CTkLabel(parent, image=graph_photo)
        graph_label.image = graph_photo  # Keep a reference to avoid garbage collection
        graph_label.pack(pady=20)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Game Price Predictor")
    root.geometry("800x600")
    GameScreen(root)
    root.mainloop()