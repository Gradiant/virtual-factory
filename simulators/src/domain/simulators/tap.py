from src.domain.simulators.outputable import OutputAble


class Tap(OutputAble):

    def __init__(self, params: dict):
        super().__init__(params)

    def internal_run(self):
        super().internal_run()

        if __debug__:
            print("TAP: {} - current-output:{} ".format(self._name, self.current_output_level))
