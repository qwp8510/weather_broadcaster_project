from os import path
import logging
from time import sleep

from utils import get_json_content
from weather_broadcaster import WeatherBroadcaster
from model import get_notification_model


logger = logging.getLogger(__name__)
CURRENT_PATH = path.dirname(path.abspath(__file__))
time = 15 * 60


def main():
    user_data = get_json_content(path.join(CURRENT_PATH, 'user_data.json'))
    weather_broadcaster = WeatherBroadcaster(owm_api_key=user_data.get('owm_api_key'))
    for user, user_info in user_data['users'].items():
        try:
            if user_info.get('model_type') == 'PrecipitationModelNotification':
                model = get_notification_model(user_info.get('model_type'))
                model(weather_broadcaster, user_info)
        except Exception as err:
            logger.error('fail with model {} error: {}'.format(
                user_info.get('model_type'), err))
    while True:
        try:
            weather_broadcaster.notify()
            sleep(time)
        except KeyboardInterrupt:
            logger.warning('keyboard interrupt\n')
            break
        except Exception as e:
            logger.error('main exception: {}'.format(e))
            break


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s')
    main()
