from src.domain.isimulatorconnectorclient import ISimulatorConnectorClient
from src.infrastructure.simulators_connection.simulatormqttclient import SimulatorMQTTClient
from src.infrastructure.simulators_connection.simulatornoneclient import SimulatorNoneClient


class SimulatorClientConnectFactory:

    @staticmethod
    def get_connector_client(params: dict) -> ISimulatorConnectorClient:
        if "type" in params:
            _type = params["type"]
            if _type == "mqtt":
                return SimulatorClientConnectFactory._get_mqtt_client(params["mqtt"])
            if _type == "none":
                return SimulatorClientConnectFactory._get_none_client()
        return SimulatorClientConnectFactory._get_none_client()

    @staticmethod
    def _get_mqtt_client(params: dict) -> SimulatorMQTTClient:
        return SimulatorMQTTClient(params)

    @staticmethod
    def _get_none_client() -> SimulatorNoneClient:
        return SimulatorNoneClient()
