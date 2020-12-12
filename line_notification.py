import requests
import logging
from base_notification import BaseNotificationInterface

from utils import trans_temp_kelvin_to_Celsius


logger = logging.getLogger(__name__)


class LineNotification(BaseNotificationInterface):
    LINE_URL = 'https://notify-api.line.me/api/notify'

    def __init__(self, line_token):
        self._line_token = line_token

    def notify(self, msg):
        headers = {'Authorization': 'Bearer ' + self._line_token}
        payload = {'message': str(msg)}
        response = requests.post(self.LINE_URL, headers=headers, params=payload)
        return response.status_code


class GeneralModelNotification(LineNotification):
    def __init__(self, weather_station, user_data):
        self.user_data = user_data
        weather_station.register_weather_station(user_data.get('user'), self)
        super().__init__(line_token=user_data.get('line_token'))

    def notify(self, msg):
        logger.info('user: {} GeneralModel notify message: {}'.format(
            self.user_data.get('user', 'NAME_IS_NEEDED'), msg))
        return super().notify(self.enrich_message(msg))

    def enrich_message(self, msg):
        return str({
            'temperature': trans_temp_kelvin_to_Celsius(
                msg.get('temperature', {}).get('temp', 'Null')),
            'humidity': msg.get('humidity', 'Null'),
            'rain': msg.get('rain') if msg.get('rain') else 0
        })


class PremiumModelNotification(LineNotification):
    def __init__(self, weather_station, user_data):
        self.user_data = user_data
        weather_station.register_weather_station(user_data.get('user'), self)
        super().__init__(line_token=user_data.get('line_token'))

    def notify(self, msg):
        logger.info('user: {} PremiumModel notify message: {}'.format(
            self.user_data.get('user', 'NAME_IS_NEEDED'), msg))
        return super().notify(self.enrich_message(msg))

    def enrich_message(self, msg):
        return str({
            'temperature': trans_temp_kelvin_to_Celsius(
                msg.get('temperature', {}).get('temp', 'Null')),
            'humidity': msg.get('humidity', 'Null'),
            'rain': msg.get('rain') if msg.get('rain') else 0,
            'status': msg.get('status', 'Null'),
            'wind speed': msg.get('wind', {}).get('speed', 'Null')
        })
