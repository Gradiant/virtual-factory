import traceback

import paho.mqtt.client as mqtt
import json
from src.domain.isimulatorconnectorclient import ISimulatorConnectorClient


class SimulatorMQTTClient(ISimulatorConnectorClient):

    def __init__(self, params: dict):
        self._mqttc = mqtt.Client()
        self._params = params
        self._connected = False
        self._connect()


    def _connect(self):
        self._connected = False
        try:
            self._mqttc.connect(self._params.get("host", "localhost"), self._params.get("port", 1883),
                                self._params.get("keepalive", 60),
                                self._params.get("bind_address", ""))
            self._mqttc.loop_start()
            self._connected = True
        except:
            self._connected = False

    def send(self, topic: str, msg: dict):
        if not self._connected:
            self._connect()
        if self._connected:
            try:
                msg.update({"sender": topic})
                self._mqttc.publish(topic, json.dumps(msg))
            except Exception:
                if __debug__:
                    traceback.print_exc()

    def subscribe(self, topic: str, callback):
        def __mqtt_callback(client, userdata, message):
            try:
                if __debug__:
                    print("{0}: mensaje recibido: {1}".format(message.topic, message.payload))
                obj = json.loads(message.payload)
                callback(obj)
            except Exception:
                if __debug__:
                    traceback.print_exc()

        try:
            self._mqttc.subscribe(topic)
            self._mqttc.message_callback_add(topic, __mqtt_callback)
        except Exception:
            if __debug__:
                traceback.print_exc()