import requests
from PIL import Image
from io import BytesIO

def get_player_image(player_id):
    # Create the URL for the player's image
    player_image_url = f'https://images.fotmob.com/image_resources/playerimages/{player_id}.png'
    
    # Send a GET request to download the image
    response = requests.get(player_image_url)
    
    # If the request was successful, open and return the image
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        print("Image not found or unable to retrieve.")
        return None

def get_team_logo(team_id):
    team_logo = f'https://images.fotmob.com/image_resources/logo/teamlogo/{team_id}.png'
    response = requests.get(team_logo)
     
    # If the request was successful, open and return the image
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        print("Image not found or unable to retrieve.")
        return None