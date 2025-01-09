import customtkinter as ctk
from helpers.databasehelper import DatabaseHelper

class AdminDashboardScreen:
    def __init__(self, parent, db_helper):
        self.parent = parent
        self.db_helper = db_helper
        self.create_table()

    def create_table(self):
        """
        Fetches the logged-in users and displays them in a table.
        """
        users = self.get_logged_in_users()

        for widget in self.parent.winfo_children():
            widget.destroy()

        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        if users:
            table_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
            table_frame.grid(row=0, column=0, padx=20, pady=20)

            headers = ["Steam ID", "Username", "Last Login"]
            for col, header in enumerate(headers):
                header_label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), text_color="white")
                header_label.grid(row=0, column=col, padx=10, pady=5)

            for row, user in enumerate(users, start=1):
                for col, value in enumerate(user):
                    value_label = ctk.CTkLabel(table_frame, text=str(value), font=("Arial", 12), text_color="white")
                    value_label.grid(row=row, column=col, padx=10, pady=5)
        else:
            error_label = ctk.CTkLabel(
                self.parent,
                text="No logged-in users found.",
                font=("Arial", 14),
                text_color="red"
            )
            error_label.grid(row=0, column=0, padx=20, pady=20)

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