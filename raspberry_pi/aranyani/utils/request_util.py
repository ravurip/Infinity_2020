import requests
from base64 import b64encode

from aranyani.config.config import rest_endpoint
from aranyani.config.logger import log


class Communicator:

    def __init__(self):
        self.rest_endpoint = rest_endpoint
        log.info(f"Initialized Cloud communicator. All the Audio clips and communications will be made to {self.rest_endpoint}")

    def __send_request(self, message):
        return requests.post(self.rest_endpoint, json=message)

    def push_audio_file(self, metadata, wavefile):
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
