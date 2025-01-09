import webbrowser
import requests
from flask import Flask, request
import logging
import os
import datetime
from helpers.databasehelper import DatabaseHelper
from dotenv import load_dotenv

load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

app = Flask(__name__)
steam_id = None
login_callback = None

DB_CONFIG = {
    "host": "108.143.125.97",
    "database": "SteamDatabase",
    "user": "postgres",
    "password": "1GratjeMooiBeest"
}
db_helper = DatabaseHelper(DB_CONFIG)


def get_rfid_user_info():
    """
    Retrieves the last successful login from the loginattempts table and fetches the user profile.
    Returns user information if found and otherwise returns none.
    """
    with db_helper.connect() as cursor:
        cursor.execute("""
            SELECT steamid FROM loginattempts
            ORDER BY datetime DESC LIMIT 1
        """)
        result = cursor.fetchone()
        if result:
            steam_id = result[0]
            return fetch_user_info(steam_id)
    return None


def fetch_user_info(steam_id):
    """
    Fetch user info from the Steam API using the given steam_id.
    Returns a dictionary with user information if successful, otherwise none.
    """
    user_info_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
    response = requests.get(user_info_url)
    if response.status_code == 200:
        user_data = response.json()
        if user_data and 'response' in user_data and user_data['response']['players']:
            player = user_data['response']['players'][0]
            return {
                "username": player["personaname"],
                "steam_id": steam_id,
                "avatar_url": player["avatarfull"]
            }
    return None


def log_user_login(user_info):
    """
    Logs or updates the users login information in the users_logins table.
    """
    with db_helper.connect() as cursor:
        steam_id = user_info["steam_id"]
        username = user_info["username"]
        last_login = datetime.datetime.now()

        cursor.execute("SELECT id FROM users_logins WHERE steam_id = %s", (steam_id,))
        if cursor.fetchone():
            cursor.execute(
                "UPDATE users_logins SET username = %s, last_login = %s WHERE steam_id = %s",
                (username, last_login, steam_id)
            )
        else:
            cursor.execute(
                "INSERT INTO users_logins (steam_id, username, last_login) VALUES (%s, %s, %s)",
                (steam_id, username, last_login)
            )


@app.route("/verify")
def verify():
    """
    Callback route for Steam OpenID verification.
    Extracts the Steam ID, fetches user info, logs the login, and calls our login callback.
    """
    global steam_id
    steam_id_url = request.args.get("openid.claimed_id")
    if steam_id_url:
        steam_id = steam_id_url.split("/")[-1]
        user_info = fetch_user_info(steam_id)
        if user_info:
            log_user_login(user_info)
            if login_callback:
                login_callback(user_info)
            return "Login successful! You can close this tab."
        else:
            return "Failed to retrieve user info.", 400
    return "Login failed", 400


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


def set_login_callback(callback):
    """
    Sets the callback function that will be triggered after a successful login.
    """
    global login_callback
    login_callback = callback


def start_flask():
    """
    Starts the Flask server.
    """
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(port=5069, host="127.0.0.1")