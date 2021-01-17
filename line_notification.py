import requests
from abc import ABC, abstractmethod


class LineNotification(ABC):
    LINE_URL = 'https://notify-api.line.me/api/notify'

    def __init__(self, line_token):
        self._line_token = line_token

    @abstractmethod
    def _enrich_message(self):
        pass

    def notify(self, msg):
        headers = {'Authorization': 'Bearer ' + self._line_token}
        payload = {'message': str(msg)}
        response = requests.post(self.LINE_URL, headers=headers, params=payload)
        return response.status_code
