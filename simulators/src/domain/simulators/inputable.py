from src.domain.simulators.simulator import Simulator


class InputAble(Simulator):

    def __init__(self, params: dict):
        Simulator.__init__(self, params)
        self.input_level = params.get("input_level", 1000)
        self._inputs = params.get("inputs", [])
        self.current_input_level = self.input_level
        self.input_blocked = False
        self.notify()
        for _input in self._inputs:
            self.subscribe(_input.get_name(), _input.callback_subscription)

    def internal_run(self):
        self.calculate_input_level()
        self.notify()

    def calculate_input_level(self):
        calc_input_level = 0
        if not self.input_blocked:
            # aquí solo sumamos los outputs de cada input
            for _input in self._inputs:
                if not _input.get_output_blocked():
                    calc_input_level += _input.get_output_level()
        # solo va a poder tener el máximo que acepta
        self.current_input_level = calc_input_level if calc_input_level <= self.input_level else self.input_level

    def get_msg_to_notify(self) -> dict:
        return {"input_level": self.input_level, "input_blocked": self.input_blocked}
