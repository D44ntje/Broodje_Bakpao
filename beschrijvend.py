import json
from collections import Counter

# Specificeer het pad naar je JSON-bestand
json_file_path = r'C:\Users\Gebruiker\OneDrive - ASG\Documenten\HU\steam.json'

# Laad de gegevens uit het JSON-bestand
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract prices from the data
prices = []
for item in data:
    price = item.get('price')
    if price is not None and price != '0.0':  # Zorg ervoor dat we geen gratis games meenemen
        prices.append(float(price))

# Functie om het gemiddelde te berekenen
def calculate_mean(prices):
    return sum(prices) / len(prices)

# Functie om de mediaan te berekenen
def calculate_median(prices):
    sorted_prices = sorted(prices)
    n = len(sorted_prices)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_prices[mid - 1] + sorted_prices[mid]) / 2
    else:
        return sorted_prices[mid]

# Functie om de modus te berekenen
def calculate_mode(prices):
    price_counts = Counter(prices)
    max_count = max(price_counts.values())
    modes = [price for price, count in price_counts.items() if count == max_count]
    return modes[0] if modes else None  # Return the first mode

# Functie om de standaarddeviatie te berekenen
def calculate_std_dev(prices, mean):
    variance = sum((x - mean) ** 2 for x in prices) / len(prices)
    return variance ** 0.5

# Bereken beschrijvende statistieken
if prices:
    mean_price = calculate_mean(prices)
    median_price = calculate_median(prices)
    mode_price = calculate_mode(prices)
    std_dev_price = calculate_std_dev(prices, mean_price)
    min_price = min(prices)
    max_price = max(prices)

    # Print de resultaten
    print(f"Gemiddelde prijs: {mean_price:.2f}")
    print(f"Mediaan prijs: {median_price:.2f}")
    print(f"Modus prijs: {mode_price:.2f}")
    print(f"Standaarddeviatie prijs: {std_dev_price:.2f}")
    print(f"Minimale prijs: {min_price:.2f}")
    print(f"Maximale prijs: {max_price:.2f}")
else:
    print("Geen prijzen beschikbaar om statistieken te berekenen.")