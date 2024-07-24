import json
import requests

URL = "https://graph.facebook.com/v20.0/"
URL_VIDEO = "https://rupload.facebook.com/video-upload/v20.0/"


def load_credentials():
    with open('credentialsPage.json', 'r') as f:
        return json.load(f)['pages']


def create_base_url(page_id, type_publish):
    return f"{URL}{page_id}/{type_publish}"


def post_request(url, data, files=None):
    try:
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return e


def main(option):
    credentials = load_credentials()
    page = credentials[option]
    page_id = page['id']
    global token
    token = page['token']
    transfer = post_request(create_base_url(page_id, 'videos'),
                            data={
                                "access_token": token,
                                "title": "Video TikTok",
                                "description": "Video de TikTok",
                            },
                            files={'video_file_chunk': open("video_tiktok.mp4", 'rb')})
    print(transfer)
