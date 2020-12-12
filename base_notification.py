from abc import ABC, abstractmethod


class BaseNotificationInterface(ABC):
    @abstractmethod
    def notify(self, msg):
        pass
