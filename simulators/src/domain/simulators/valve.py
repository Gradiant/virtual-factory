from src.domain.simulators.pipe import Pipe


class Valve(Pipe):

    def __init__(self, params):
        super().__init__(params)
        self._open = params.get("open", True)
        if not self._open:
            self.close()
        else:
            self.open()

    def open(self):
        self._open = True
        self.input_blocked = False
        self.output_blocked = False
        if __debug__:
            print("Válvula: {} - open {}".format(self._name, self._open))

    def close(self):
        self._open = False
        self.input_blocked = True
        self.output_blocked = True
        if __debug__:
            print("Válvula: {} - open {}".format(self._name, self._open))

    def internal_run(self):
        info = self.read_industrial_info(self.get_read_info_for_industry())
        value_open = info.get("open")
        if value_open is not None:
            if value_open:
                self.open()
            else:
                self.close()
        info = self.write_industrial_info(self.get_write_info_for_industry())
        super().internal_run()

        if __debug__:
            print("Válvula: {} - open {}, current_input: {}, current_output:{}".format(self._name, self._open,
                                                                                       self.current_input_level,
                                                                                       self.current_output_level))

    def get_read_info_for_industry(self) -> list:
        return ["open"]

    def get_write_info_for_industry(self) -> dict:
        return {"open": self._open}
