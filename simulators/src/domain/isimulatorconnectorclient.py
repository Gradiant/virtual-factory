from abc import abstractmethod


class ISimulatorConnectorClient:

    @abstractmethod
    def send(self, topic: str, msg: dict):
        raise NotImplemented

    @abstractmethod
    def subscribe(self, topic: str, callback):
        raise NotImplemented
