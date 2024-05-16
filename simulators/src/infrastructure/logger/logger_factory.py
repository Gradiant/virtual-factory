from src.domain.ilogger import ILogger
from src.infrastructure.logger.csvlog import CSVLog
from src.infrastructure.logger.nonelog import NoneLog
from src.infrastructure.logger.opensearchlog import OpensearchLog
from src.infrastructure.logger.printlog import PrintLog


class LoggerFactory:

    @staticmethod
    def get_logger(params: dict) -> ILogger:
        type = params.get("type", "none")
        if type == "none":
            return NoneLog()
        elif type == "print":
            return PrintLog()
        elif type == "csv":
            return CSVLog(params.get("csv"))
        elif type == "opensearch":
            return OpensearchLog(params.get("opensearch"))
        else:
            return NoneLog()
