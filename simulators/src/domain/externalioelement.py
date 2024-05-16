from src.domain.externalinputelement import ExternalInputElement
from src.domain.externaloutputelement import ExternalOutputElement


class ExternalIOElement(ExternalInputElement, ExternalOutputElement):

    def __init__(self, name: str):
        ExternalInputElement.__init__(self, name)
        ExternalOutputElement.__init__(self, name)

    def callback_subscription(self, msg: dict):
        self._input_level = msg.get("input_level")
        self._input_blocked = msg.get("input_blocked")
        self._output_level = msg.get("output_level")
        self._output_blocked = msg.get("output_blocked")
