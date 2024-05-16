from src.domain.simulators.flowable import FlowAble


class Pipe(FlowAble):

    def __init__(self, params: dict):
        super().__init__(params)

    def calculate_output_level(self):
        # aqui ya se calcula la variable self._current_input_level
        super().calculate_input_level()
        # la característica de la PIPE es que tiene de flujo lo mismo que el input (en condiciones de no bloqueo)
        n_outputs_0 = 0
        if not self.output_blocked:
            # aquí no sirve sumar ya que algunos pueden estar llenos/bloqueados,
            # y por lo tanto hay que desviar el flujo a los demás outputs.
            for _output in self._outputs:
                if _output.get_input_blocked() or _output.get_input_level() == 0:
                    n_outputs_0 += 1
            if n_outputs_0 != len(self._outputs):
                # es es el valor que le corresponderá a cada uno por igual
                # (los que están bloqueados, lo ignorarán, porque tienen el input a 0)
                self.current_output_level = self.current_input_level / (len(self._outputs) - n_outputs_0)
            else:
                self.current_output_level = 0.0
        else:
            self.current_output_level = 0.0

        self.output_level = self.current_output_level
