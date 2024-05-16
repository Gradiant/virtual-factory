from random import choices
from string import hexdigits

from src.domain.externalelement import ExternalElement


class ExternalBuggingElement(ExternalElement):

    def __init__(self, target_name: str):
        super().__init__(f'{target_name}_bug')
        self._bug_params = {}

    def get_bug_params(self) -> dict:
        return self._bug_params

    def set_bug_params(self, params: dict):
        self._bug_params = params

    def callback_subscription(self, msg: dict):
        if msg is None:
            msg = {}
            self.set_bug_params(msg)
        else:
            while True:
                new_key = ''.join(choices(hexdigits, k=4))
                if self._bug_params.get(new_key) is None:
                    break
            self._bug_params.update({new_key: msg})
