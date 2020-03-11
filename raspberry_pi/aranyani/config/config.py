import os
from datetime import datetime

def get_home_directory():
    try:
        return os.environ['ARANYANI_HOME']
    except KeyError:
        return "/home/pi/aranyani/"


def get_current_date():
    return datetime.now().strftime("%Y/%m/%d")


def get_rest_endpoint(zone: str = "none"):
    return "https://ohpq8lw7m4.execute-api.ap-south-1.amazonaws.com/Dev"


AUDIO_SAMPLE_RECORD = {'CHUNK': 128, 'RATE': 48000, 'TO_CACHE': 1500}

rest_endpoint = get_rest_endpoint()

aranyani_home_dir = get_home_directory()

application_logs_dir = aranyani_home_dir + "/logs"
application_data_dir = aranyani_home_dir + "/data"
application_temp_dir = aranyani_home_dir + "/temp"


#'CRITICAL','FATAL','ERROR','WARNING','INFO','DEBUG'
log_level = "INFO"
log_filename = application_logs_dir + f"/aranyani.log"

