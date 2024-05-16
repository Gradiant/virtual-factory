from src.domain.ilogger import ILogger


class PrintLog(ILogger):

    def to_log(self, msg: dict):
        print(msg)
