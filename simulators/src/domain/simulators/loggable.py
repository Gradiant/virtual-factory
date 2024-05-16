
from src.infrastructure.logger.logger_factory import LoggerFactory
from src.infrastructure.logger.nonelog import NoneLog


class Loggable:

    def __init__(self, params: dict):
        self._config = params.get("logging", {})
        self._dont_log_variables = ['_thread', '_simulator_connector_client', '_industrial_client',
                                    '_dont_log_variables', '_logger_element', '_logging', '_bugging_element',
                                    '_inputs', '_outputs']

        self._logging = self._config.get("logging", False)
        self._logger = LoggerFactory.get_logger(self._config) if self._logging else NoneLog()
