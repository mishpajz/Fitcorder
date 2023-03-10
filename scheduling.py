import pickle
import os
import apscheduler
import time
import jobs
from apscheduler.schedulers.background import BackgroundScheduler

urls = {
    "T9-155": "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
    "T9-105": "http://cdn.streaming.cesnet.cz/fa-cvut/fa-12/playlist.m3u8",
    "T9-107": "http://cdn.streaming.cesnet.cz/fa-cvut/fa-13/playlist.m3u8",
    "TK-BS": "https://cdn.streaming.cesnet.cz/fa-cvut/fit-01/playlist.m3u8"
}

schedules = {}
for key in urls:
    schedules[key] = BackgroundScheduler()

#times = ['7:30', '9:15', '11:00', '12:45', '14:30', '16:15', '18:00', '19:45']

times = ['16:55', '17:00', '14:38', '14:38', '14:38', '14:40', '14:42', '14:38']

def store_data(data, filename):
    # create a relative path to the config directory
    filepath = os.path.join("config", filename)
    try:
        # check if the config directory exists
        if not os.path.exists("config"):
            # create a new directory
            os.mkdir("config")
        # open the file for writing
        file = open(filepath, "wb")
        # write the dictionary to the file
        pickle.dump(data, file)
    except Exception as e:
        # handle any other exception
        print(f"An error occurred: {e}")
    finally:
        # close the file if it is opened
        if "file" in locals():
            file.close()

def load_data(filename):
    # create a relative path to the config directory
    filepath = os.path.join("config", filename)
    try:
        # open the file for reading
        file = open(filepath, "rb")
        # load the dictionary from the file
        data = pickle.load(file)
    except Exception as e:
        # handle any other exception
        print(f"An error occurred: {e}")
    finally:
        # close the file if it is opened
        if "file" in locals():
            file.close()
            return data

def add_jobs(target):
    data = load_data(target)
    if not data: # check if data is empty
        data = {} # create an empty dictionary

    schedules[target].remove_all_jobs()

    for key in data:
        for i_str in data[key]:
            i = int(i_str)
            hours = int(times[i].split(':')[0])
            minutes = int(times[i].split(':')[1])

            job = schedules[target].add_job(jobs.job, 
                                            'cron', 
                                            args=[urls[target]], 
                                            day_of_week=key,
                                            hour=hours,
                                            minute=minutes)
            
    for job in schedules[target].get_jobs():
        print(job)
            