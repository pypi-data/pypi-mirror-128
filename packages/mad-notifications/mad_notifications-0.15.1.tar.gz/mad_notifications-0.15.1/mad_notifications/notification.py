from mad_notifications.models import get_notification_model

class Notification:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
        self.kwargs = kwargs

    def notify(self):
        try:
            return get_notification_model().objects.create(**self.kwargs)
        except Exception as e:
            raise
