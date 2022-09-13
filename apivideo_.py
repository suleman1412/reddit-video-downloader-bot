import requests,configparser
import apivideo
from apivideo.apis import VideosApi

config = configparser.ConfigParser()
config.read('auth.ini')
API_KEY = config.get('credentials', 'api.video_api')

def upload_video(title):

# Set up variables for endpoints
    auth_url = "https://ws.api.video/auth/api-key"
    create_url = "https://ws.api.video/videos"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "apiKey": API_KEY
    }

    response = requests.request("POST", auth_url, json=payload, headers=headers)
    response = response.json()
    token = response.get("access_token")

    auth_string = "Bearer " + token


    # Set up headers for authentication
    headers_bearer = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": auth_string
    }

    # Create a video container
    payload2 = {
        "title": title,
    }

    response = requests.request("POST", create_url, json=payload2, headers=headers_bearer)
    response = response.json()
    videoId = response["videoId"]

    # Create endpoint to upload video to
    upload_url = " https://ws.api.video/videos" + "/" + videoId + "/source"

    # Create upload video headers
    headers_upload = {
        "Accept": "application/vnd.api.video+json",
        "Authorization": auth_string
    }

    file = {"file": open("output.mp4", "rb")}
    response = requests.request("POST", upload_url, files=file, headers=headers_upload)
    json_response = response.json()
    mp4_url = json_response['assets']['mp4']
    return mp4_url

