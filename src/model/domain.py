import requests


class Domain:
    def __init__(self):
        self.url = str()
        self.name = str()
        self.connectionTimeout = int()
        self.connectionWait = int()
        self.connectionAttempts = int()
        self.connectionHeader = str()

    def obtainSource(self, url: str()):
        attempts = self.connectionAttempts
        srcPage = requests.get(url, headers=self.connectionHeader,
                               timeout=self.connectionTimeout)
