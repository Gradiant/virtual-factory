from abc import abstractmethod

from src.domain.isimulatorconnectorclient import ISimulatorConnectorClient


class Notifier:

    def __init__(self, params: dict):
        self._name = params.get("name")
        self._simulator_connector_client = self.__init_simulator_connector_singleton(
            params.get("simulator_connector_client"))

    def __init_simulator_connector_singleton(self, simulator_client: ISimulatorConnectorClient):
        try:
            self._simulator_connector_client
        except AttributeError:
            self._simulator_connector_client = simulator_client

        return self._simulator_connector_client

    def get_name(self) -> str:
        return self._name

    @abstractmethod
    def get_msg_to_notify(self):
        raise NotImplemented

    def notify(self):
        self._simulator_connector_client.send(self._name, self.get_msg_to_notify())

    def subscribe(self, name: str, callback):
        self._simulator_connector_client.subscribe(name, callback)
