from src.domain.ilogger import ILogger


class NoneLog(ILogger):
    def to_log(self):
        pass
