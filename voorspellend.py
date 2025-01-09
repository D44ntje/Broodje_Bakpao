import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator

json_file_path = r'C:\Users\Gebruiker\OneDrive - ASG\Documenten\HU\steam.json'

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

names = []
developers = []
publishers = []
categories = []
owners = []
prices = []

most_expensive_game = None
highest_price = 0
all_games_data = []

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
            developers.append(item['developer'])
            publishers.append(item['publisher'])
            categories.append(item['categories'])
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

games_data = list(zip(names, owners, prices))
most_popular_games = sorted(games_data, key=lambda x: int(x[1].split(' - ')[0]) if ' - ' in x[1] else int(x[1].replace(',', '')), reverse=True)[:5]
most_expensive_games = sorted(all_games_data, key=lambda x: float(x[2]), reverse=True)[:5]

print("\nTop 5 Most Popular Games:")
for game in most_popular_games:
    if ' - ' in game[1]:
        lower_bound = int(game[1].split(' - ')[0])
        predicted_price = predict(lower_bound)
    else:
        predicted_price = predict(int(game[1].replace(',', '')))
    price_display = "Free" if float(game[2]) == 0.0 else game[2]
    print(f"Name: {game[0]}, Owners: {game[1]}, Actual Price: {price_display}, Price by AI: {predicted_price:.2f}")

print("\nTop 5 Most Expensive Games:")
for game in most_expensive_games:
    if ' - ' in game[1]:
        lower_bound = int(game[1].split(' - ')[0])
        predicted_price = predict(lower_bound)
    else:
        predicted_price = predict(int(game[1].replace(',', '')))
    price_display = "Free" if float(game[2]) == 0.0 else game[2]
    print(f"Name: {game[0]}, Owners: {game[1]}, Actual Price: {price_display}, Price by AI: {predicted_price:.2f}")

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
plt.show()

print("\nPrice by AI is based on the calculation, y= b _0 + b_1·x, with use of linear regression.")