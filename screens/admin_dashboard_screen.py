import customtkinter as ctk
from helpers.databasehelper import DatabaseHelper

class AdminDashboardScreen:
    def __init__(self, parent, db_helper, go_back_callback):
        self.parent = parent
        self.db_helper = db_helper
        self.go_back_callback = go_back_callback

        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(parent, fg_color="#171A21")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        section_frame = ctk.CTkFrame(self.main_frame, fg_color="#1B2838", corner_radius=10)
        section_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        section_frame.grid_rowconfigure(0, weight=1)
        section_frame.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(section_frame, width=600, height=400, fg_color="#171A21", corner_radius=10)
        self.scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.back_button = ctk.CTkButton(
            section_frame,
            text="Back",
            command=self.go_back_callback,
            width=100,
            fg_color="#2A475E",
            hover_color="#1B2838"
        )
        self.back_button.pack(side="bottom", pady=10)

        self.create_table()

    def create_table(self):
        """
        Fetches the logged-in users and displays them.
        """
        users = self.get_logged_in_users()

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if users:
            headers = ["Steam ID", "Username", "Last Login"]
            header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=10, pady=5)

            for col, header in enumerate(headers):
                header_label = ctk.CTkLabel(header_frame, text=header, font=("Arial", 14, "bold"), text_color="white")
                header_label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

            for row, user in enumerate(users, start=1):
                row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1B2838", corner_radius=10)
                row_frame.pack(fill="x", padx=10, pady=5)

                for col, value in enumerate(user):
                    value_label = ctk.CTkLabel(row_frame, text=str(value), font=("Arial", 12), text_color="white")
                    value_label.grid(row=0, column=col, padx=10, pady=5, sticky="w")
        else:
            error_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No logged-in users found.",
                font=("Arial", 14),
                text_color="red"
            )
            error_label.pack(pady=20)

    def get_logged_in_users(self):
        """
        Fetches the list of users who have logged in and is ordered by the last login time.
        """
        try:
            with self.db_helper.connect() as cursor:
                cursor.execute("SELECT steam_id, username, last_login FROM users_logins ORDER BY last_login DESC")
                users = cursor.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching logged-in users: {e}")
            return []