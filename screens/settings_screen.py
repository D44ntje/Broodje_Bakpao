import customtkinter as ctk
from PIL import Image  # Import PIL for image handling
import login
from login import get_user_info
import threading


class SettingsScreen:

    def __init__(self, parent, logout_callback):
        self.parent = parent  # Save the parent widget
        self.logout_callback = logout_callback  # Save the logout callback

        # Clear parent widget before adding new elements
        self.clear_parent()

        # Main label
        self.main_label = ctk.CTkLabel(parent, text="Settings Screen", font=("Arial", 24), text_color="white")
        self.main_label.pack(pady=20)

        # Create a frame to center the textboxes
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(pady=20)

        # User info
        self.label_user = ctk.CTkLabel(self.frame, width=300, text="This is your user information:")
        self.label_user.pack(pady=5)

        # Fetch user information dynamically
        user_info = self.get_user_information()

        # Display Username
        username_text = user_info.get('username', 'No username available')
        self.label1 = ctk.CTkLabel(self.frame, width=300, text=f"Username: {username_text}")
        self.label1.pack(pady=5)

        # Display Steam ID
        steam_id_text = user_info.get('steam_id', 'No Steam ID available')
        self.label2 = ctk.CTkLabel(self.frame, width=300, text=f"Steam ID: {steam_id_text}")
        self.label2.pack(pady=5)

        self.label3 = ctk.CTkLabel(self.frame, width=300, text="Thank you for using us!\nFeel free to donate any amount at any time.")
        self.label3.pack(pady=5)

        # Load and display the image
        tikkie_code = "icons/support_tikkie.png"  # Path to your image
        try:
            # Open the image using PIL
            image = Image.open(tikkie_code)

            # Create a CTkImage object from the loaded image
            tikkie_image = ctk.CTkImage(light_image=image, dark_image=image, size=(250, 250))

            # Create a label to display the image
            ctk.CTkLabel(self.frame, image=tikkie_image, text="").pack(pady=20)

        except Exception as e:
            print(f"Error loading image: {e}")

        # Log Out button
        self.logout_button = ctk.CTkButton(parent, text="Log Out", command=self.logout)
        self.logout_button.pack(side="bottom", pady=20)

    def get_user_information(self):
        """Fetch user information from the login module."""
        try:
            user_info = get_user_info()
            if user_info:
                return user_info
            return {}
        except Exception as e:
            print(f"Error fetching user information: {e}")
            return {}

    def clear_parent(self):
        """Clear all widgets from the parent container."""
        for widget in self.parent.winfo_children():
            widget.destroy()

    def logout(self):
        """Invoke the logout callback."""
        if self.logout_callback:
            self.logout_callback()

    def exit_app(self):
        """Close the application."""
        self.parent.quit()  # Ends the Tkinter event loop
        self.parent.destroy()  # Destroys the main window and all child widgets


# Example usage:
if __name__ == "__main__":
    def example_logout():
        print("Logged out!")

    # Start the Flask server in a separate thread for login functionality
    threading.Thread(target=login.start_flask, daemon=True).start()

    # Start the application
    app = ctk.CTk()
    app.geometry("400x400")
    SettingsScreen(app, example_logout)
    app.mainloop()
