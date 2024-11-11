from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Define configuration variables
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
