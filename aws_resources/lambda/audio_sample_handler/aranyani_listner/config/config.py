from datetime import datetime

S3_BUCKET = 'gupthas-garage'

AUDIO_FILES_PATH = 'infinity/aranyani/'


def get_current_date():
    return datetime.now().strftime("%Y/%m/%d")
