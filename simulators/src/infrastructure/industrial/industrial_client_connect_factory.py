from src.domain.iindustrialconnectorclient import IIndustrialConnectorClient
from src.infrastructure.industrial.industrialmodbusclient import IndustrialModbusClient


class IndustrialClientConnectFactory:

    @staticmethod
    def get_connector_client(params: dict) -> IIndustrialConnectorClient:
        if "type" in params:
            _type = params["type"]
            if _type == "modbus":
                return IndustrialClientConnectFactory._get_modbus_client(params["modbus"])
        raise NotImplemented

    @staticmethod
    def _get_modbus_client(params: dict) -> IndustrialModbusClient:
        return IndustrialModbusClient(params)
