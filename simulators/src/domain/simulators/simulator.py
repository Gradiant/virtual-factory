from abc import abstractmethod
from datetime import datetime

from src.domain.notifier import Notifier
from src.domain.runable import RunAble
from src.domain.industrial import Industrial
from src.domain.simulators.buggable import Buggable
from src.domain.simulators.loggable import Loggable


class Simulator(RunAble, Notifier, Industrial, Buggable, Loggable):

    def __init__(self, params: dict):
        RunAble.__init__(self)
        Notifier.__init__(self, params)
        Industrial.__init__(self, params)
        Buggable.__init__(self, params)
        Loggable.__init__(self, params)
        self._dont_log_variables = ['_thread', '_running', '_simulator_connector_client',
                                    '_industrial_client',
                                    '_dont_log_variables',
                                    '_logger_element',
                                    '_bugging_element', '_buggable', '_buggable_notifier', '_bug_threads',
                                    '_inputs', 'input_level',
                                    'current_input_level', 'input_blocked',
                                    '_outputs', 'output_level', 'current_output_level', 'output_blocked',
                                    "_mapper_industry_properties",
                                    "_config", "_logger", '_logging']

    def run_thread(self):
        self.internal_run()
        if self._buggable:
            self.create_bug()
        if self._logging:
            self._logger.to_log(self.dict_for_log())

    @abstractmethod
    def internal_run(self):
        pass

    def get_msg_to_notify(self):
        return {}

    def dict_for_log(self) -> dict:
        temp_dict = self.__dict__.copy()
        running_bugs = [*temp_dict['_bug_threads']]
        temp_dict['running_bugs'] = running_bugs

        for var in self._dont_log_variables:
            if var in temp_dict:
                del temp_dict[var]

        ret_dict = {}
        for key, value in temp_dict.items():
            new_key = key
            if new_key.startswith("_"):
                new_key = new_key[1:]
            if type(value) in [list, dict]:
                ret_dict[new_key] = False if len(value) == 0 else value
            else:
                ret_dict[new_key] = value

        ret_dict["timestamp"] = datetime.utcnow().isoformat()

        return ret_dict
