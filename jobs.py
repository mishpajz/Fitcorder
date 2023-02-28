import yt_dlp
import time
import multiprocessing
import os
from datetime import datetime
from signal import SIGINT

RETRIES = 5
LENGTH = 60 * (60 + 30 + 5)
COOKIES = os.path.join("config", "cookies.txt")
FILENAME = "prednaska-"

ydl_opts = {
    'cookiefile': COOKIES,
    'wait_for_video': (60, 60 * 5),
    'outtmpl': FILENAME,
    'external_downloader': 'ffmpeg',
    'nopart': True
}
    

def download_video(url):
    for i in range(RETRIES):
        try:
            file_name = FILENAME + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + url.split('/')[-2] + '.mp4'
            ydl_opts['outtmpl'] = os.path.join("volume", file_name)
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            error_code = ydl.download(url)
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(60)
            continue


def job(on):
    print("Recording from " + on)
    proc = multiprocessing.Process(target=download_video, args=[on])
    proc.start()
    time.sleep(LENGTH)
    os.kill(proc.pid, SIGINT) # yt-dlp stream needs to be closed with signint to perform cleanup