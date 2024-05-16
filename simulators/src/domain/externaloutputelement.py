from src.domain.externalelement import ExternalElement


class ExternalOutputElement(ExternalElement):

    def __init__(self, name: str):
        super().__init__(name)
        self._output_level = 0
        self._output_blocked = False

    def get_output_level(self) -> float:
        return self._output_level

    def get_output_blocked(self) -> bool:
        return self._output_blocked

    def callback_subscription(self, msg: dict):
        self._output_level = msg.get("output_level")
        self._output_blocked = msg.get("output_blocked")
