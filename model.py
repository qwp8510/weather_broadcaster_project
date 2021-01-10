from notifications import GeneralModelNotification
from notifications import PremiumModelNotification
from notifications import PrecipitationModelNotification


def get_notification_model(model_type):
    if model_type == 'PremiumModelNotification':
        return PremiumModelNotification
    elif model_type == 'PrecipitationModelNotification':
        return PrecipitationModelNotification
    else:
        return GeneralModelNotification
