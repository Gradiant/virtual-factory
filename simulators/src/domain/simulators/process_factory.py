from src.application.flamingmoesprocess.flamingmoeprocess import FlamingMoesProcess
from src.domain.process import Process

class ProcessFactory:
    @staticmethod
    def get_process(params: dict) -> Process:
        if "type" in params:
            _type = params["type"].lower()
            if _type == "flamingmoes":
                return ProcessFactory._get_flamingMoes(params)

        raise NotImplemented

    @staticmethod
    def _get_flamingMoes(params: dict) -> Process:
        return FlamingMoesProcess(params)
