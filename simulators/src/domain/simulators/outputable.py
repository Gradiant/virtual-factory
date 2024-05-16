from src.domain.simulators.simulator import Simulator


class OutputAble(Simulator):

    def __init__(self, params: dict):
        super().__init__(params)
        self.output_level = params.get("output_level", 0.0)
        self.current_output_level = 0.0
        self._outputs = params.get("outputs", [])
        self.output_blocked = False
        for _output in self._outputs:
            self.subscribe(_output.get_name(), _output.callback_subscription)

    def internal_run(self):
        self.calculate_output_level()
        self.notify()

    def set_output_level(self, value: float):
        self.output_level = value

    def calculate_output_level(self):
        n_outputs_blocked = 0
        if not self.output_blocked:
            # aquí no sirve sumar ya que algunos pueden estar llenos/bloqueados,
            # y por lo tanto hay que desviar el flujo a los demás outputs.
            for _output in self._outputs:
                if _output.get_input_blocked() or _output.get_input_level() == 0:
                    n_outputs_blocked += 1
            if n_outputs_blocked != len(self._outputs):
                # es es el valor que le corresponderá a cada uno por igual
                # (los que están bloqueados, lo ignorarán, porque tienen el input a 0)
                # Ojito porque igual parece que tiene que poner todo su maximo posible, pero no, es la parta proporcional
                self.current_output_level = self.output_level / (len(self._outputs) - n_outputs_blocked)
            else:
                self.current_output_level = 0.0
        else:
            self.current_output_level = 0.0

    def get_msg_to_notify(self):
        return {"output_level": self.current_output_level, "output_blocked": self.output_blocked}
