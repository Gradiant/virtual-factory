from enum import Enum

from src.domain.process import Process


class FlamingMoesProcessState(Enum):
    WAITFORTANK1_2 = 1
    FILLING_TANKS_1_2 = 2
    HEATING_TANKS_1_2 = 3
    WAITING_FOR_RECOLETOR = 4
    FILLING_RECOLECTOR = 5
    COOLING_RECOLECTOR = 6
    FILL_BOTTLES = 7


class FlamingMoesProcess(Process):

    def __init__(self, params: dict):
        super().__init__(params)
        self._tequila_valve_open = False
        self._peppermint_valve_open = False
        self._mintcream_valve_open = False
        self._brandy_valve_open = False
        self._gin_valve_open = False
        self._coughsyrup_valve_open = False
        self._mixtank1_valve_open = False
        self._mixtank2_valve_open = False
        self._recolector_valve_open = False
        self._bottle_on = False
        self._mixtank1_heat_cool_level = 0
        self._mixtank2_heat_cool_level = 0
        self._recolector_heat_cool_level = 0
        self._manual_mode = True
        self._mixtank1_capacity = 0
        self._mixtank1_temp = 0
        self._mixtank2_capacity = 0
        self._mixtank2_temp = 0
        self._recolector_capacity = 0
        self._recolector_temp = 0
        self._state = FlamingMoesProcessState.WAITFORTANK1_2

    def internal_run(self):
        info = self.read_industrial_info(self.get_read_info_for_industry())
        self._manual_mode = info.get("manual_mode", True)
        self._mixtank1_capacity = info.get("mixtank1_capacity", 0)
        self._mixtank1_temp = info.get("mixtank1_temp", 0)
        self._mixtank2_capacity = info.get("mixtank2_capacity", 0)
        self._mixtank2_temp = info.get("mixtank2_temp", 0)
        self._recolector_capacity = info.get("recolector_capacity", 0)
        self._recolector_temp = info.get("recolector_temp", 0)

        if not self._manual_mode:
            self.run_automatic_process()
            self.write_industrial_info(self.get_write_info_for_industry())

    def run_automatic_process(self):
        switch_state = {
            FlamingMoesProcessState.WAITFORTANK1_2: self._waiting_for_tank1_2,
            FlamingMoesProcessState.FILLING_TANKS_1_2: self._filling_tank1_2,
            FlamingMoesProcessState.HEATING_TANKS_1_2: self._heating_tank1_2,
            FlamingMoesProcessState.WAITING_FOR_RECOLETOR: self._waiting_for_recolector,
            FlamingMoesProcessState.FILLING_RECOLECTOR: self._filling_recolector,
            FlamingMoesProcessState.COOLING_RECOLECTOR: self._cooling_recolector,
            FlamingMoesProcessState.FILL_BOTTLES: self._fill_bottles,
        }

        next = switch_state.get(self._state, None)
        if next is not None:
            next()

    def _waiting_for_tank1_2(self):
        print("waiting_for_tank1_2")
        # las temperaturas de los tanques deben estar en 6 grados y deben estar vacios
        if self._mixtank1_temp == 6 and self._mixtank2_temp == 6 and \
                self._mixtank1_capacity == 0 and self._mixtank2_capacity == 0:
            self._state = FlamingMoesProcessState.FILLING_TANKS_1_2
        else:
            self._set_mixtank1_temp_to(6)
            self._set_mixtank2_temp_to(6)
            self._empty_mixtank1(0)
            self._empty_mixtank2(0)

    def _filling_tank1_2(self):
        print("filling_tank1_2")
        # se llenan a partes iguales hasta que los tanques alcancen los 90
        if self._mixtank1_capacity >= 90 and self._mixtank2_capacity >= 90:
            self._state = FlamingMoesProcessState.HEATING_TANKS_1_2
        else:
            self._set_mixtank1_temp_to(6)
            self._set_mixtank2_temp_to(6)
            self._fill_mixtank1(90)
            self._fill_mixtank2(90)

    def _heating_tank1_2(self):
        print("heating_tank1_2")
        # se enfria hasta 0 grados
        if self._mixtank1_temp == 20 and self._mixtank2_temp == 20:
            self._state = FlamingMoesProcessState.WAITING_FOR_RECOLETOR
        else:
            self._set_mixtank1_temp_to(20)
            self._set_mixtank2_temp_to(20)
            self._fill_mixtank1(90)
            self._fill_mixtank2(90)

    def _waiting_for_recolector(self):
        print("waiting_for_recolector")
        # el recolector tiene que obtener la mezcla a 0 grados y estar vacío
        if self._recolector_capacity == 0 and self._recolector_temp == 20:
            self._state = FlamingMoesProcessState.FILLING_RECOLECTOR
        else:
            self._set_mixtank1_temp_to(20)
            self._set_mixtank2_temp_to(20)
            self._fill_mixtank1(90)
            self._fill_mixtank2(90)
            self._set_recolector_temp_to(20)
            self._empty_recolector(0)

    def _filling_recolector(self):
        print("filling_recolector")
        # se llenan a partes iguales hasta que se vacíen los tankes 1 y 2
        if self._mixtank1_capacity == 0 and self._mixtank2_capacity == 0:
            self._state = FlamingMoesProcessState.COOLING_RECOLECTOR
            self._mixtank1_valve_open = False
            self._mixtank2_valve_open = False
        else:
            self._bottle_on = False
            self._set_mixtank1_temp_to(20)
            self._set_mixtank2_temp_to(20)
            self._set_recolector_temp_to(20)
            self._empty_mixtank1(0)
            self._empty_mixtank2(0)

    def _cooling_recolector(self):
        print("cooling_recolector")
        # se calienta el recolector hasta 6 grados
        if self._recolector_temp == 6:
            self._state = FlamingMoesProcessState.FILL_BOTTLES
        else:
            self._set_recolector_temp_to(6)

    def _fill_bottles(self):
        print("fill bottles")
        if self._recolector_capacity == 0:
            self._state = FlamingMoesProcessState.WAITFORTANK1_2
        else:
            self._set_recolector_temp_to(6)
            self._empty_recolector(0)

    def _set_mixtank1_temp_to(self, temperature: int):
        if self._mixtank1_temp > temperature:
            self._mixtank1_heat_cool_level = -1
        elif self._mixtank1_temp < temperature:
            self._mixtank1_heat_cool_level = 1
        else:
            self._mixtank1_heat_cool_level = 0

    def _set_mixtank2_temp_to(self, temperature: int):
        if self._mixtank2_temp > temperature:
            self._mixtank2_heat_cool_level = -1
        elif self._mixtank2_temp < temperature:
            self._mixtank2_heat_cool_level = 1
        else:
            self._mixtank2_heat_cool_level = 0

    def _set_recolector_temp_to(self, temperature: int):
        if self._recolector_temp > temperature:
            self._recolector_heat_cool_level = -1
        elif self._recolector_temp < temperature:
            self._recolector_heat_cool_level = 1
        else:
            self._recolector_heat_cool_level = 0

    def _fill_mixtank1(self, capacity: int):
        self._mixtank1_valve_open = False
        if self._mixtank1_capacity < capacity:
            self._tequila_valve_open = True
            self._peppermint_valve_open = True
            self._mintcream_valve_open = True
        else:
            self._tequila_valve_open = False
            self._peppermint_valve_open = False
            self._mintcream_valve_open = False

    def _empty_mixtank1(self, capacity: int):
        self._tequila_valve_open = False
        self._peppermint_valve_open = False
        self._mintcream_valve_open = False
        self._mixtank1_valve_open = True
        if self._mixtank1_capacity <= capacity:
            self._mixtank1_valve_open = False

    def _fill_mixtank2(self, capacity: int):
        self._mixtank2_valve_open = False
        if self._mixtank2_capacity < capacity:
            self._brandy_valve_open = True
            self._gin_valve_open = True
            self._coughsyrup_valve_open = True
        else:
            self._brandy_valve_open = False
            self._gin_valve_open = False
            self._coughsyrup_valve_open = False

    def _empty_mixtank2(self, capacity: int):
        self._brandy_valve_open = False
        self._gin_valve_open = False
        self._coughsyrup_valve_open = False
        self._mixtank2_valve_open = True
        if self._mixtank2_capacity <= capacity:
            self._mixtank2_valve_open = False

    def _fill_recollector(self, capacity: int):
        self._recolector_valve_open = False
        self._bottle_on = False
        if self._recolector_valve_open < capacity:
            self._mixtank2_valve_open = True
            self._mixtank1_valve_open = True
        else:
            self._mixtank2_valve_open = False
            self._mixtank1_valve_open = False

    def _empty_recolector(self, capacity: int):
        self._mixtank2_valve_open = False
        self._mixtank1_valve_open = False
        self._recolector_valve_open = True
        self._bottle_on = True
        if self._recolector_capacity <= capacity:
            self._recolector_valve_open = False
            self._bottle_on = False

    @staticmethod
    def get_read_info_for_industry() -> list:
        return ["manual_mode",
                "mixtank1_capacity", "mixtank1_temp",
                "mixtank2_capacity", "mixtank2_temp",
                "recolector_capacity", "recolector_temp"]

    def get_write_info_for_industry(self) -> dict:
        return {"tequila_valve_open": self._tequila_valve_open,
                "peppermint_valve_open": self._peppermint_valve_open,
                "mintcream_valve_open": self._mintcream_valve_open,
                "brandy_valve_open": self._brandy_valve_open,
                "gin_valve_open": self._gin_valve_open,
                "coughsyrup_valve_open": self._coughsyrup_valve_open,
                "mixtank1_valve_open": self._mixtank1_valve_open,
                "mixtank2_valve_open": self._mixtank2_valve_open,
                "recolector_valve_open": self._recolector_valve_open,
                "mixtank1_heat_cool_level": self._mixtank1_heat_cool_level,
                "mixtank2_heat_cool_level": self._mixtank2_heat_cool_level,
                "recolector_heat_cool_level": self._recolector_heat_cool_level,
                "bottleon": self._bottle_on
                }
