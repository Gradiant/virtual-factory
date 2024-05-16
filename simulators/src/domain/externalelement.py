from abc import abstractmethod


class ExternalElement:

    def __init__(self, name: str):
        self._name = name

    def get_name(self):
        return self._name

    @abstractmethod
    def callback_subscription(self, msg: dict):
        raise NotImplemented
