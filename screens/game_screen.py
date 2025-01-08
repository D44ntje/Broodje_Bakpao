import customtkinter as ctk

class GameScreen:
    def __init__(self, parent):
        # title of the screen
        ctk.CTkLabel(parent, text="Game Screen", font=("Arial", 24), text_color="white").pack(pady=20)

        # creating and placing a searchbar
        self.search_bar = ctk.CTkEntry(parent, placeholder_text="Search for a game...")
        self.search_bar.pack(pady=(0, 20), padx=10, fill="x")

        # adding segments to the screen
        self.add_expanding_segment(parent, "Recommended by friends", "This section shows games recommended by your friends.")
        self.add_expanding_segment(parent, "Top 10 worldwide", "Explore the top 10 trending games worldwide.")

    # creates a container holding two labels, 1 with title and 1 with description
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

    # button actions
    def recommended_by_friends(self):
        print("Recommended by friends clicked")

    def top_10_worldwide(self):
        print("Top 10 worldwide clicked")
