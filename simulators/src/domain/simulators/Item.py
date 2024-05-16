class Item():

    def __init__(self, params: dict):
        self._code = params.get("_code")
        self._width = params.get("_width")
        self._height = params.get("_height")
        self._weight = params.get("_weight")

    @property
    def code(self):
        return self._code

    @property
    def width(self):
        return self._width

    @property
    def heigth(self):
        return self._height

    @property
    def weight(self):
        return self._width

    def __str__(self):
        return self._code
