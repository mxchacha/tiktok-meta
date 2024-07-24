import json
import time
import requests

URL = "https://graph.facebook.com/v20.0/"
URL_VIDEO = "https://rupload.facebook.com/video-upload/v20.0/"


def load_credentials():
    with open('credentialsPage.json', 'r') as f:
        return json.load(f)['pages']


def initialize_upload_session(page_valid, token_valid):
    try:
        response = requests.post(f"{URL}{page_valid}/video_reels", {
            "upload_phase": "start",
            "access_token": token_valid,
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al inicializar la sesión de carga: {e}")
        return None


def upload_video(video_id, token_valid):
    try:
        headers = {
            "Authorization": 'OAuth ' + token_valid,
            "offset": "0",
            "file_size": str(get_video_size("video_tiktok.mp4")),
        }
        with open('video_tiktok.mp4', 'rb') as f:
            response = requests.post(URL_VIDEO + '' + video_id, headers=headers, data=f)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al cargar el video: {e}")
        return None


def get_video_size(video_path="video_tiktok.mp4"):
    try:
        with open(video_path, 'rb') as video_file:
            return len(video_file.read())
    except Exception as e:
        print(f"Error al obtener el tamaño del archivo de video: {e}")
        return None


def check_upload_status(video_id, token_valid):
    try:
        response = requests.get(f"{URL}{video_id}", {
            "fields": "status",
            "access_token": token_valid,
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al verificar el estado de la carga: {e}")
        return None


def publish_reel(video_id, page_valid, token_valid):
    try:
        response = requests.post(f"{URL}{page_valid}/video_reels", params={
            "access_token": token_valid,
            "video_id": video_id,
            "upload_phase": "finish",
            "video_state": "PUBLISHED",
            "description": "#reel #follow #love #funny #meme #comedy #happy #loveyou – #teamo #trending #duet – #duo  #fashion #meme"
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al publicar el reel: {e}")
        return None


def main(option):
    credentials = load_credentials()
    if option not in credentials:
        print("Invalid option")
        return
    page_valid = credentials[option]['id']
    token_valid = credentials[option]['token']
    upload_session = initialize_upload_session(page_valid, token_valid)
    if upload_session:
        video_id = upload_session["video_id"]
        result = upload_video(video_id, token_valid)
        print(result)
        time.sleep(5)
        if result:
            publish_result = publish_reel(video_id, page_valid, token_valid)
            print(publish_result)
            time.sleep(1)
            print(check_upload_status(video_id, token_valid))
        else:
            print("Error al cargar el video")
    else:
        print("Error al inicializar la sesión de carga")
