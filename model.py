from line_notification import GeneralModelNotification
from line_notification import PremiumModelNotification
from line_notification import PrecipitationModelNotification


def get_notification_model(model_type):
    if model_type == 'PremiumModelNotification':
        return PremiumModelNotification
    elif model_type == 'PrecipitationModelNotification':
        return PrecipitationModelNotification
    else:
        return GeneralModelNotification
