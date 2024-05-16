from src.domain.simulators.flowable import FlowAble


class Tank(FlowAble):

    def __init__(self, params: dict):
        super().__init__(params)

        self._temp = params.get("temp", 0)
        self._max_temp = params.get("max_temp", self._temp)
        self._min_temp = params.get("min_temp", 0)
        self._heat_cool_level = params.get("heat_cool_level", 0)

        self._capacity = params.get("capacity", 100)
        self._max_capacity = params.get("max_capacity", self._capacity)
        self._min_capacity = 0

        self._pressure = params.get("pressure", 1)
        self._max_pressure = params.get("max_pressure", self._pressure)
        self._min_pressure = 0

        self._print_info()

    def _print_info(self):
        if __debug__:
            print(
                "TANK:{} - temp:{}, max_temp:{}, min_temp:{}, heat_cool_level:{}, capacity:{}, max_capacity:{}, min_capacity:{}, pressure:{}, max_pressure:{}, min_pressure:{}".format(
                    self._name, self._temp, self._max_temp, self._min_temp, self._heat_cool_level, self._capacity,
                    self._max_capacity,
                    self._min_capacity, self._pressure, self._max_pressure, self._min_pressure))

    def calcular_presion(self):
        # Ojo, como no tengo datos suficientes (altura del tanque, tipo de líquido o gas, moles etc)
        # hago algo para que vaya cambiando en función de capacidad y temperatura

        new_capacity_amount = self.current_input_level - self.current_output_level
        new_capacity = self._capacity + new_capacity_amount

        new_temp_amount = self._heat_cool_level / 10
        new_temp = self._temp + new_temp_amount

        if new_capacity_amount != 0 or new_temp_amount != 0:
            pressure1 = 0 if new_capacity_amount == 0 else 0.1 if new_capacity_amount > 0 else -0.1
            pressure2 = 0 if new_temp_amount == 0 else 0.1 if new_temp_amount > 0 else -0.1
            new_pressure_amount = pressure1 + pressure2
            new_pressure = self._pressure + new_pressure_amount

            if new_pressure >= self._max_pressure:
                self._pressure = self._max_pressure
                if __debug__:
                    print("válvula de emergencia activada, la presión llegó al máximo")
            elif new_pressure <= self._min_pressure:
                self._pressure = self._min_pressure
                if __debug__:
                    print("válvula de emergencia activada, la presión llegó al mínimo")
            else:
                self._pressure = new_pressure

    def calcular_temp(self):
        new_temp_amount = self._heat_cool_level / 10
        new_temp = self._temp + new_temp_amount
        if new_temp >= self._max_temp:
            self._temp = self._max_temp
            if __debug__:
                print(
                    "Se llegó a la temperatura más alta soportada, activado el enfriamiento de emergencia para evitar que siga aumentando")
        if new_temp <= self._min_temp:
            self._temp = self._min_temp
            if __debug__:
                print(
                    "Se llegó a la temperatura más baja soportada, activando el calentador de emergencia para evitar que siga disminuyendo")
        else:
            self._temp = new_temp

    def calcular_capacidad(self):
        new_capacity_amount = self.current_input_level - self.current_output_level
        new_capacity = self._capacity + new_capacity_amount

        if new_capacity >= self._max_capacity:
            if __debug__:
                print("{}: Se llegó a la máxima capacidad: {}".format(self._name, self._max_capacity))
            self._capacity = self._max_capacity
            self.input_blocked = True
        elif new_capacity <= self._min_capacity:
            if __debug__:
                print("{}:Se llegó a la mínima capacidad: {}".format(self._name, self._min_capacity))
            self._capacity = self._min_capacity
            self.output_blocked = True
        else:
            if __debug__:
                print("{}:llenando:{}".format(self._name, new_capacity_amount))
            self._capacity = new_capacity
            "por si estaban bloqueados, ya le podemos decir que no lo están"
            self.input_blocked = False
            self.output_blocked = False

    def internal_run(self):
        info = self.read_industrial_info(self.get_read_info_for_industry())
        self._heat_cool_level = info.get("heat_cool_level", 0)
        self.calculate_levels()
        self.calcular_capacidad()
        self.calcular_temp()
        self.calcular_presion()
        self._print_info()
        self.notify()
        self.write_industrial_info(self.get_write_info_for_industry())

    @staticmethod
    def get_read_info_for_industry() -> list:
        return ["heat_cool_level"]

    def get_write_info_for_industry(self) -> dict:
        return {"max_capacity": self._max_capacity,
                "min_capacity": self._min_capacity,
                "capacity": self._capacity,
                "max_temp": self._max_temp,
                "min_temp": self._min_temp,
                "temp": self._temp,
                "max_pressure": self._max_pressure,
                "min_pressure": self._min_pressure,
                "pressure": self._pressure}

    def get_temp(self) -> float:
        return self._temp

    def get_capacity(self) -> float:
        return self._capacity

    def get_pressure(self) -> float:
        return self._pressure

    def set_heat_cool_level(self, value: int = 0):
        self._heat_cool_level = value

    def get_heat_cool_level(self) -> int:
        return self._heat_cool_level
