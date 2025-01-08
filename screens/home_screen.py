import requests
import customtkinter as ctk
import webbrowser


class HomeScreen:
    def __init__(self, parent):
        # Configure parent grid
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(parent, fg_color="#171A21")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid layout
        self.main_frame.grid_rowconfigure(0, weight=0)  # Title row has less weight
        self.main_frame.grid_rowconfigure((1, 2), weight=0)  # Disable weight for other sections
        self.main_frame.grid_rowconfigure(1, weight=1)  # Allow the first row (news section) to fill space
        self.main_frame.grid_columnconfigure((0, 1), weight=1)  # Two columns

        # Add title
        title = ctk.CTkLabel(self.main_frame, text="Home Screen", font=("Arial", 24, "bold"), text_color="white")
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")  # Reduce bottom padding to raise sections

        # Create sections
        self.create_sections()

    def create_sections(self):
        # Section 1 - Latest News Section (scrollable, fills entire space)
        section1 = ctk.CTkFrame(self.main_frame, fg_color="#1B2838", corner_radius=10)
        section1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew",
                      columnspan=2)  # Fill entire row (expand across two columns)

        ctk.CTkLabel(section1, text="Latest News", font=("Arial", 16), text_color="white").pack(pady=10)

        # Create a scrollable frame inside the section for news items
        self.scrollable_frame = ctk.CTkScrollableFrame(section1, width=400, fg_color="#171A21", corner_radius=10)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create a frame for the refresh button to avoid grid/pack conflict
        button_frame = ctk.CTkFrame(section1, fg_color="#171A21", height=50)
        button_frame.pack(fill="x", pady=10)  # Pack button frame horizontally at the top

        # Refresh Button (to reload news)
        refresh_button = ctk.CTkButton(button_frame, text="Refresh", command=self.refresh_news)
        refresh_button.pack(side="right", padx=(0, 10))  # Align button to the right

        # Fetch Steam news initially
        self.load_steam_news()

    def load_steam_news(self):
        # Clear existing news content (to refresh)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Steam News Hub API endpoint
        news_url = 'https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/'

        # Example: List of App IDs (e.g., Team Fortress 2, Dota 2)
        app_ids = [440, 730, 570]  # 440 = Team Fortress 2, 730 = CS:GO, 570 = Dota 2

        try:
            for app_id in app_ids:
                response = requests.get(news_url, params={
                    'appid': app_id,
                    'count': 5,  # Number of articles
                    'maxlength': 500,  # Max length of article content
                    'format': 'json'
                })
                news_data = response.json()

                # Check if 'newsitems' exist in the response
                if 'newsitems' in news_data['appnews']:
                    for article in news_data['appnews']['newsitems']:
                        # Ensure that it's Steam-related content
                        if 'url' in article and 'title' in article:
                            # Create a frame for each news article (horizontal layout)
                            article_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1B2838", corner_radius=10)
                            article_frame.pack(padx=10, pady=10, fill="x", expand=True)

                            # Title of article
                            title = article['title']
                            ctk.CTkLabel(article_frame, text=title, font=("Arial", 22, "bold"),
                                         text_color="white").pack(side="top", anchor="w", padx=10, pady=10)

                            # Summary with a line break
                            summary = article['contents']
                            self.display_summary(article_frame, summary)

                            # Read more link
                            read_more = article['url']
                            ctk.CTkButton(article_frame, text="Read more",
                                          command=lambda url=read_more: self.open_url(url)).pack(pady=10)

        except Exception as e:
            ctk.CTkLabel(self.scrollable_frame, text=f"Failed to load news: {str(e)}", font=("Arial", 12),
                         text_color="red").pack(pady=10)

    @staticmethod
    def display_summary(article_frame, summary):
        # Split summary into words
        words = summary.split(' ')

        # Process the words in chunks of 20
        chunk_size = 20
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            ctk.CTkLabel(article_frame, text=chunk.strip(), font=("Arial", 12), text_color="white").pack(pady=2,
                                                                                                         padx=10)

    @staticmethod
    def open_url(url):
        webbrowser.open(url)

    def refresh_news(self):
        # Fetch fresh data by calling load_steam_news again
        print("Refreshing news...")
        self.load_steam_news()
