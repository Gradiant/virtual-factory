class FlowableToBeltElement():

    def __init__(self, name: str, params: dict):
        self._name = name
        self._position = params.get("position")

