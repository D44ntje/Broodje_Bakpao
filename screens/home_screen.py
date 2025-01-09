import requests
import customtkinter as ctk
import webbrowser
from html import unescape
from bs4 import BeautifulSoup

class HomeScreen:
    def __init__(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(parent, fg_color="#171A21")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        title = ctk.CTkLabel(self.main_frame, text="Home Screen", font=("Arial", 24, "bold"), text_color="white")
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

        self.create_sections()

    def create_sections(self):
        section1 = ctk.CTkFrame(self.main_frame, fg_color="#1B2838", corner_radius=10)
        section1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        ctk.CTkLabel(section1, text="Latest News", font=("Arial", 25), text_color="white").pack(pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(section1, width=400, fg_color="#171A21", corner_radius=10)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.refresh_button = ctk.CTkButton(section1, text="Refresh", command=self.refresh_news)
        self.refresh_button.place(relx=0.98, rely=0.02, anchor="ne")

        self.load_steam_news()

    def load_steam_news(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        news_url = 'https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/'
        app_ids = [440, 570, 730, 945360, 1091500, 1172470, 292030, 578080]
        displayed_articles = set()

        try:
            for app_id in app_ids:
                response = requests.get(news_url, params={
                    'appid': app_id,
                    'count': 5,
                    'maxlength': 500,
                    'format': 'json'
                })
                news_data = response.json()

                if 'newsitems' in news_data['appnews']:
                    for article in news_data['appnews']['newsitems']:
                        if article['url'] in displayed_articles:
                            continue
                        displayed_articles.add(article['url'])

                        article_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1B2838", corner_radius=10)
                        article_frame.pack(padx=10, pady=10, fill="x", expand=True)

                        title = self.split_text(article['title'], 10)
                        ctk.CTkLabel(article_frame, text=title, font=("Arial", 20, "bold"), text_color="white").pack(pady=5)

                        content = self.strip_html(article['contents'])
                        ctk.CTkLabel(article_frame, text=content, font=("Arial", 12), text_color="white", wraplength=380).pack(pady=5)

                        link_button = ctk.CTkButton(article_frame, text="Read More", command=lambda url=article['url']: webbrowser.open(url))
                        link_button.pack(pady=5)
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")

    def refresh_news(self):
        self.load_steam_news()

    @staticmethod
    def strip_html(html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        return unescape(soup.get_text())

    @staticmethod
    def split_text(text, words_per_line):
        words = text.split()
        lines = [' '.join(words[i:i + words_per_line]) for i in range(0, len(words), words_per_line)]
        return '\n'.join(lines)
