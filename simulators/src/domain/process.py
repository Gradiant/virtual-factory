from abc import abstractmethod

from src.domain.industrial import Industrial
from src.domain.runable import RunAble


class Process(RunAble, Industrial):

    def __init__(self, params: dict):
        RunAble.__init__(self)
        Industrial.__init__(self, params)

    def run_thread(self):
        self.internal_run()

    @abstractmethod
    def internal_run(self):
        pass
