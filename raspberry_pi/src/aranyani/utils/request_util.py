import json
import requests
from base64 import b64encode

from aranyani.config.config import rest_endpoint, HOSTNAME
from aranyani.config.logger import log

from pprint import pprint

class Communicator:

    def __init__(self):
        self.rest_endpoint = rest_endpoint
        log.info(
            f"Initialized Cloud communicator. All the Audio clips and communications will be made to {self.rest_endpoint}")

    def __convert_python_dict_to_json(self, message):
        return json.dumps(message)

    def __send_request(self, message):
        try:
            json_message = self.__convert_python_dict_to_json(message) #TODO
            return requests.post(self.rest_endpoint, json=json_message, timeout=30000)

        except Exception as exc:
            log.error("Failed to send message to cloud", exc)
            return None

    def push_audio_file(self, audio_data, metadata=None):
        message = {}

        message['eventType'] = 'audio'
        message['metadata'] = {"hostname": HOSTNAME}
        message['data'] = audio_data

        return self.__send_request(message)

    def send_heart_beat(self):
        pass
