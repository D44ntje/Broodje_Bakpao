import customtkinter as ctk

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

        # labeles stacked vertically
        self.label1 = ctk.CTkLabel(self.frame, width=300, text="label 1")
        self.label1.pack(pady=5)

        self.label2 = ctk.CTkLabel(self.frame, width=300, text="label 2")
        self.label2.pack(pady=5)

        self.label3 = ctk.CTkLabel(self.frame, width=300, text="label 3")
        self.label3.pack(pady=5)

        self.label4 = ctk.CTkLabel(self.frame, width=300, text="label 4")
        self.label4.pack(pady=5)

        # Log Out button beneath the textboxes
        self.logout_button = ctk.CTkButton(parent, text="Log Out", command=self.logout)
        self.logout_button.pack(side="bottom", pady=20)

    def clear_parent(self):
        """Clear all widgets from the parent container."""
        for widget in self.parent.winfo_children():
            widget.destroy()

    def logout(self):
        """Invoke the logout callback."""
        if self.logout_callback:
            self.logout_callback()

# Example usage:
if __name__ == "__main__":
    def example_logout():
        print("Logged out!")

    app = ctk.CTk()
    app.geometry("400x400")
    SettingsScreen(app, example_logout)
    app.mainloop()
