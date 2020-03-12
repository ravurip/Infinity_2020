import json
import requests
from base64 import b64encode

from aranyani.config.config import rest_endpoint
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
            json_message = self.__convert_python_dict_to_json(message)
            return requests.post(self.rest_endpoint, json=json_message, timeout=29000)

        except Exception as exc:
            log.error("Failed to send message to cloud")
            return None

    def push_audio_file(self, audio_data, metadata=None):
        message = {}

        message['metadata'] = {"hostname": "rasp"}
        message['audio_particulars'] = audio_data

        return self.__send_request(message)

    def send_heart_beat(self):
        pass

#     from base64 import b64encode, b64decode
#     a = open("/home/pradeepr/IdeaProjects/Infinity_2020/raspberry_pi/sample_5.wav", "rb").read()
#
#     #wav bytes 2 wav str
#     b = b64encode(a)
#     c = b.decode()
#     #wav str back 2 wav bytes
#     d = c.encode()
#     e = b64decode(d)
#
#     open("temp.wav", "wb").write(e)
