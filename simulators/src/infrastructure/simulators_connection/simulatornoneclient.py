from src.domain.isimulatorconnectorclient import ISimulatorConnectorClient


class SimulatorNoneClient(ISimulatorConnectorClient):

    def __init__(self):
        pass

    def send(self, topic: str, msg: dict):
        pass

    def subscribe(self, topic: str, callback):
        pass