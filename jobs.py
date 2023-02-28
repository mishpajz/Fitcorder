import yt_dlp
import time
import multiprocessing
import os
from datetime import datetime

LENGTH = 60 * (60 + 30)
COOKIES = os.path.join("config", "cookies.txt")
FILENAME = "prednaska-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".mp4"
FILEPATH = os.path.join("volume", FILENAME)

ydl_opts = {
    'cookiefile': COOKIES,
    'wait_for_video': (60, 60 * 5),
    'nopart': True,
    'outtmpl': FILEPATH
}
    

def download_video(url):
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    error_code = ydl.download(url)


def job(on):
    print("Recording from " + on)
    proc = multiprocessing.Process(target=download_video, args=[on])
    proc.start()
    time.sleep(LENGTH)
    proc.terminate()