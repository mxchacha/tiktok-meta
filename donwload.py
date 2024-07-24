from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests


def download_tiktok_video(tiktok_url, download_path):
    global driver
    try:
        # Configurar el controlador de Chrome
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Ejecutar en modo headless para no abrir una ventana del navegador
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-extensions")

        driver = webdriver.Chrome(service=service, options=options)

        # Abrir la página web que permite descargar videos de TikTok sin marca de agua
        driver.get("https://snaptik.app/en1")

        # Encontrar el campo de entrada y pegar la URL del video de TikTok
        input_field = driver.find_element(By.ID, 'url')
        input_field.send_keys(tiktok_url)
        input_field.send_keys(Keys.RETURN)

        # Esperar a que aparezca el botón de descarga
        download_button = None
        for _ in range(10):  # Intentar hasta 10 veces esperando 1 segundo cada vez
            try:
                download_button = driver.find_element(By.XPATH, '//a[contains(@class, "button download-file")]')
                break
            except Exception as e:
                time.sleep(1)

        if not download_button:
            raise Exception("No se pudo encontrar el botón de descarga después de varios intentos.")

        # Obtener la URL de descarga
        download_url = download_button.get_attribute("href")

        # Descargar el video usando requests
        video_data = requests.get(download_url).content
        with open(download_path, 'wb') as video_file:
            video_file.write(video_data)

        print(f"Video descargado con éxito en {download_path}")

    except Exception as e:
        print(f"Error al descargar el video de TikTok: {e}")

    finally:
        if driver:
            driver.quit()


def execute(url):
    download_tiktok_video(url, "video_tiktok.mp4")


if __name__ == "__main__":
    tiktok_url = "https://vm.tiktok.com/ZMrBS58NR/"  # Reemplaza con la URL del video de TikTok
    download_tiktok_video(tiktok_url, "video_tiktok.mp4")
