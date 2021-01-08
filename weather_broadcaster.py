import logging
from os import path

from weather_station import WeatherStation


CURRENT_PATH = path.dirname(path.abspath(__file__))
logger = logging.getLogger(__name__)


class WeatherBroadcaster(WeatherStation):
    def __init__(self, owm_api_key=None):
        super().__init__(owm_api_key=owm_api_key)
        self.user_models = {}

    def register_weather_station(self, user, model):
        self.user_models.setdefault(user, model)

    def remove_weather_station(self, user):
        if self.user_models.get(user):
            del self.user_models[user]
        else:
            logger.warning('remove_weather_station fail with del unexist user: {}'.format(user))

    def notify(self):
        models = self.user_models.copy()
        for model in models.values():
            model.notify(self.get_data_by_coord(
                lon=model.user_data.get('longitude', 0), lat=model.user_data.get('latitude', 0)))
