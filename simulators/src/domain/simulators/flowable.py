from src.domain.simulators.inputable import InputAble
from src.domain.simulators.outputable import OutputAble


class FlowAble(InputAble, OutputAble):

    def __init__(self, params: dict):
        OutputAble.__init__(self, params)
        InputAble.__init__(self, params)

    def internal_run(self):
        self.calculate_levels()
        self.notify()

    def calculate_levels(self):
        self.calculate_input_level()
        self.calculate_output_level()

    def get_msg_to_notify(self):
        info = InputAble.get_msg_to_notify(self)
        info.update(OutputAble.get_msg_to_notify(self))
        return info
