import webbrowser
import requests
from flask import Flask, request
import os
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

app = Flask(__name__)
steam_id = None
login_callback = None

def open_steam_login():
    """
    Opens the Steam login page for authentication.
    """
    steam_login_url = (
        "https://steamcommunity.com/openid/login?"
        "openid.ns=http://specs.openid.net/auth/2.0&"
        "openid.mode=checkid_setup&"
        "openid.return_to=http://localhost:5069/verify&"
        "openid.realm=http://localhost:5069&"
        "openid.identity=http://specs.openid.net/auth/2.0/identifier_select&"
        "openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select"
    )
    webbrowser.open(steam_login_url)

@app.route("/verify")
def verify():
    """
    Callback route for Steam OpenID verification.
    Extracts the Steam ID and calls the login callback.
    """
    global steam_id
    steam_id_url = request.args.get("openid.claimed_id")
    if steam_id_url:
        steam_id = steam_id_url.split("/")[-1]

        # If a login callback is set, call it and pass the steam_id
        if login_callback:
            login_callback(steam_id)

        # Redirect to confirmation page
        return "Login successful! You can close this tab."
    return "Login failed", 400


def get_user_info():
    """
    Retrieves the user profile information from Steam using their Steam ID.
    Returns a dictionary with the username, Steam ID, and avatar URL.
    """
    global steam_id
    if not steam_id:
        return None

    user_info_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
    response = requests.get(user_info_url)
    user_data = response.json()

    if user_data and user_data['response']['players']:
        player = user_data['response']['players'][0]
        return {
            "username": player["personaname"],
            "steam_id": steam_id,
            "avatar_url": player["avatarfull"]
        }
    return None


def set_login_callback(callback):
    """
    Sets the callback function that will be triggered after a successful login.
    """
    global login_callback
    login_callback = callback

def start_flask():
    """
    Starts the Flask server to listen for login callbacks.
    """
    app.run(port=5069, host="127.0.0.1")
