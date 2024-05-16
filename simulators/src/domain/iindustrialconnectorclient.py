from abc import abstractmethod


class IIndustrialConnectorClient:

    @abstractmethod
    def write(self, info: dict, mapping_info: dict = None):
        raise NotImplemented

    @abstractmethod
    def read(self, info: dict) -> dict:
        raise NotImplemented
