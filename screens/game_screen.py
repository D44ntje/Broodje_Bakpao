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

    most_expensive_game = None
    highest_price = 0

    for item in data:
        price = item.get('price')
        if price is not None:
            current_price = float(price)
            if current_price > highest_price:
                highest_price = current_price
                most_expensive_game = item
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
    plt.savefig('predicted_prices_plot.png', format='png', bbox_inches='tight')
    plt.close()

class GameScreen:
    def __init__(self, parent):
        ctk.CTkLabel(parent, text="Game Screen", font=("Arial", 24), text_color="white").pack(pady=20)

        self.search_bar = ctk.CTkEntry(parent, placeholder_text="Search for a game...")
        self.search_bar.pack(pady=(0, 20), padx=10, fill="x")

        self.add_expanding_segment(parent, "Recommended by friends", "This section shows games recommended by your friends.")
        self.add_expanding_segment(parent, "Top 10 worldwide", "Explore the top 10 trending games worldwide.")

        # Generate and display the graph
        generate_graph()
        self.display_graph(parent)

    def add_expanding_segment(self, parent, title, description):
        segment_frame = ctk.CTkFrame(parent, fg_color="#2A475E", corner_radius=15)
        segment_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(
            segment_frame,
            text=title,
            font=("Arial", 16, "bold"),
            text_color="white",
            anchor="w"
        ).pack(side="top", padx=10, pady=(10, 5), fill="x")

        ctk.CTkLabel(
            segment_frame,
            text=description,
            font=("Arial", 12),
            text_color="lightgray",
            anchor="w",
            wraplength=600
        ).pack(side="top", padx=10, pady=(0, 10), fill="x")

    def display_graph(self, parent):
        # Load the saved image
        image = Image.open('predicted_prices_plot.png')
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the image
        graph_label = ctk.CTkLabel(parent, image=photo)
        graph_label.image = photo  # Keep a reference to avoid garbage collection
        graph_label.pack(pady=20)

    def recommended_by_friends(self):
        print("Recommended by friends clicked")

    def top_10_worldwide(self):
        print("Top 10 worldwide clicked")

# Example usage
if __name__ == "__main__":
    root = ctk.CTk()
    GameScreen(root)
    root.mainloop()