import requests

from aranyani.config.config import rest_endpoint
from aranyani.config.logger import log


class Communicator:

    def __init__(self):
        self.rest_endpoint = rest_endpoint
        log.info(f"Initialized Cloud communicator. All the Audio clips and communications will be made to {self.rest_endpoint}")

    def send_request(self, message):
        requests.post(self.rest_endpoint)
