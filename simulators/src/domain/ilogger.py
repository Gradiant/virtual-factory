from abc import abstractmethod


class ILogger:

    @abstractmethod
    def to_log(self, msg: dict):
        raise NotImplemented
