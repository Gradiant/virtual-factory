import traceback

from pymodbus.client import ModbusTcpClient
from src.domain.iindustrialconnectorclient import IIndustrialConnectorClient
import numpy as np


class IndustrialModbusClient(IIndustrialConnectorClient):

    def __init__(self, params: dict):
        self._modbus_client = ModbusTcpClient(
            host=params.get("host", "localhost"), port=params.get("port", 502)
        )
        self._slave = params.get("slave", 0)
        self._connected = False
        self._connect()

    def _connect(self):
        try:
            self._modbus_client.connect()
            self._connected = True
        except Exception:
            if __debug__:
                traceback.print_exc()
            self._connected = False

    def read(self, info: dict) -> dict:
        info_response = {}
        if info:
            if not self._connected:
                self._connect()
            if self._connected:
                try:
                    for info_reg in info:
                        info_response[info_reg["map"]] = self._read(info_reg)
                except Exception:
                    self._connected = False
        return info_response

    def _read(self, info_reg: dict):
        if info_reg["type"] == "coil":
            return self._modbus_client.read_coils(info_reg["map"], 1, self._slave).bits[0]
        elif info_reg["type"] == "register":
            return int(np.int16(self._modbus_client.read_holding_registers(info_reg["map"], 1, self._slave).registers[0]))
        elif info_reg["type"] == "uregister":
            return int(self._modbus_client.read_holding_registers(info_reg["map"], 1, self._slave).registers[0])
        else:
            print("Invalid register type, expected key-type : {}".format(info_reg))
        return None

    def write(self, info: dict, mapping_info: dict = None):
        if info:
            if not self._connected:
                self._connect()
            if self._connected:
                try:
                    for key, value in info.items():
                        self._write(key, value, mapping_info)
                except Exception:
                    self._connected = False

    def _write(self, key: int, value, mapping_info: dict):
        if mapping_info["type"] == "coil":
            self._modbus_client.write_coil(int(key), bool(value), self._slave)
        elif mapping_info["type"] == "register":
            self._modbus_client.write_register(int(key), int(np.uint16(value)), self._slave)
        elif mapping_info["type"] == "uregister":
            self._modbus_client.write_register(int(key), int(value), self._slave)
        else:
            print("Invalid register type, expected key-type : {}".format(mapping_info))
        return None
