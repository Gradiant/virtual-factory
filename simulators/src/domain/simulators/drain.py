from src.domain.simulators.inputable import InputAble


class Drain(InputAble):

    def __init__(self, params: dict):
        super().__init__(params)

    def internal_run(self):
        super().internal_run()
        if __debug__:
            print("DRAIN: {} - current_input: {} ".format(self._name, self.current_input_level))
