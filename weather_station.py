import pyowm
import json
import logging
from requests import Timeout
import requests


logger = logging.getLogger(__name__)
LINE_URL = 'https://notify-api.line.me/api/notify'


class WeatherStation():
    # document: https://pyowm.readthedocs.io/en/latest/pyowm.weatherapi25.html
    def __init__(self, owm_api_key=None):
        self._owm_api_key = owm_api_key
        self._owm = None

    @property
    def owm(self):
        try:
            if not self._owm:
                self._owm = pyowm.OWM(self._owm_api_key)
        except Timeout as err:
            logger.error('WeatherStation owm fail with TimeOut error {}'.format(err))
        return self._owm

    def get_data_by_coord(self, lon, lat):
        observation = self.owm.weather_at_coords(lat=lat, lon=lon)
        weather = observation.get_weather()
        return json.loads(weather.to_JSON())


def trans_temp_kelvin_to_Celsius(temp):
    return int(temp - 273.15)


def enrich_general_model(weather_data):
    return {
        'temperature': trans_temp_kelvin_to_Celsius(
            weather_data.get('temperature', {}).get('temp')),
        'humidity': weather_data.get('humidity'),
        'rain': weather_data.get('rain') if weather_data.get('rain') else 0
    }


def send_message(token, msg):
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'message': str(msg)}
    response = requests.post(LINE_URL, headers=headers, params=payload)
    return response.status_code


def send_general_model_message(token, msg):
    logger.info('GeneralModel notify message: {}'.format(msg))
    send_message(token, msg)


def main():
    api_key = 'here_is_your_owm_api_key'
    line_token = 'here_is_your_line_token'
    longitude, latitude = 121.5172, 25.0472  # Taipei Main Station
    weather_station = WeatherStation(owm_api_key=api_key)
    weather_data = weather_station.get_data_by_coord(lon=longitude, lat=latitude)
    logger.info('weather station getting lon: {}, lat:{} data:{}'.format(
        longitude, latitude, weather_data))
    general_model_msg = enrich_general_model(weather_data)
    send_general_model_message(line_token, general_model_msg)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s')
    main()
