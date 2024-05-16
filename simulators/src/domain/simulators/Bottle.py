from src.domain.simulators.Item import Item


class Bottle(Item):
    '''
    :param capacity: maximun capacity of this bottle (l)
    :type capacity: float
    :param level: currently filled. (l)
    :type level: float
    '''
    def __init__(self, params: dict):
        Item.__init__(self, params)
        self._capacity = params.get("_capacity")
        self._level = 0

    @property
    def capacity(self):
        return self._capacity

    @property
    def level(self):
        return self._level

    def fill(self, amount):
        self._level += amount
        if self._level > self._capacity:
            self._level = self._capacity

    def can_be_filled(self):
        return self.capacity > self._level

    @property
    def weight(self):
        # assuming density = 1
        return self._weight + self.level
