from src.domain.simulators.drain import Drain
from src.domain.simulators.pipe import Pipe
from src.domain.simulators.simulator import Simulator
from src.domain.simulators.tank import Tank
from src.domain.simulators.tap import Tap
from src.domain.simulators.valve import Valve
from src.domain.simulators.conveyorbelt import ConveyorBelt


class SimulatorFactory:
    @staticmethod
    def get_simulator(params: dict) -> Simulator:
        if "type" in params:
            _type = params["type"].lower()
            if _type == "tap":
                return SimulatorFactory._get_tap(params)
            if _type == "drain":
                return SimulatorFactory._get_drain(params)
            if _type == "pipe":
                return SimulatorFactory._get_pipe(params)
            if _type == "valve":
                return SimulatorFactory._get_valve(params)
            if _type == "tank":
                return SimulatorFactory._get_tank(params)
            if _type == "conveyorbelt":
                return SimulatorFactory._get_belt(params)
        raise NotImplemented

    @staticmethod
    def _get_tap(params: dict) -> Tap:
        return Tap(params)

    @staticmethod
    def _get_drain(params: dict) -> Drain:
        return Drain(params)

    @staticmethod
    def _get_pipe(params: dict) -> Pipe:
        return Pipe(params)

    @staticmethod
    def _get_valve(params: dict) -> Valve:
        return Valve(params)

    @staticmethod
    def _get_tank(params: dict) -> Tank:
        return Tank(params)

    @staticmethod
    def _get_belt(params: dict) -> ConveyorBelt:
        return ConveyorBelt(params)
