from src.domain.externalelement import ExternalElement


class ExternalInputElement(ExternalElement):

    def __init__(self, name: str):
        super().__init__(name)
        self._input_level = 0.0
        self._input_blocked = False
        self._sender = name

    def get_input_level(self) -> float:
        return self._input_level

    def get_input_blocked(self) -> bool:
        return self._input_blocked

    def callback_subscription(self, msg: dict):
        self._input_level = msg.get("input_level")
        self._input_blocked = msg.get("input_blocked")
        self._sender = msg.get("sender")
