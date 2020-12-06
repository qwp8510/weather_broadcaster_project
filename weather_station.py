import pyowm
import json
import logging
from requests import Timeout
from os import path
from abc import ABC, abstractmethod


CURRENT_PATH = path.dirname(path.abspath(__file__))
logger = logging.getLogger(__name__)
LINE_URL = 'https://notify-api.line.me/api/notify'


class Subject(ABC):
    @abstractmethod
    def register_weather_station(self, user, model):
        pass

    @abstractmethod
    def remove_weather_station(self, user):
        pass

    @abstractmethod
    def notify(self):
        pass


class WeatherStation(Subject):
    # document: https://pyowm.readthedocs.io/en/latest/pyowm.weatherapi25.html
    def __init__(self, owm_api_key=None):
        self._owm_api_key = owm_api_key
        self._owm = None
        self.user_models = {}

    def register_weather_station(self, user, model):
        self.user_models.setdefault(user, model)

    def remove_weather_station(self, user):
        if self.user_models.get(user):
            del self.user_models[user]
        else:
            logger.warning('remove_weather_station fail with del unexist user: {}'.format(user))

    def notify(self):
        for model in self.user_models.values():
            model.notify(self.get_data_by_coord(
                lon=model.user_data.get('longitude', 0), lat=model.user_data.get('latitude', 0)))

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
