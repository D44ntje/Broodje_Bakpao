from PIL import Image
from io import BytesIO
import requests
import customtkinter as ctk

def download_avatar(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = Image.open(BytesIO(response.content)).resize((150, 150))
        return ctk.CTkImage(light_image=image_data, size=(150, 150))
    except requests.RequestException:
        return None
