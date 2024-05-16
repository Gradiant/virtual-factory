class Industrial:

    def __init__(self, params: dict):
        self._industrial_client = params.get("industrial_connector_client")
        self._mapper_industry_properties = params.get("mapper_industry_properties")

    def write_industrial_info(self, info: dict):

        if self._mapper_industry_properties and "write" in self._mapper_industry_properties:

            for key, value in info.items():
                if key in self._mapper_industry_properties["write"]:
                    real_info = {
                        self._mapper_industry_properties["write"][key]["map"]: value
                    }
                    self._industrial_client.write(real_info, self._mapper_industry_properties["write"][key])
        else:
            self._industrial_client.write(info)

    def read_industrial_info(self, info: list) -> dict:
        if self._mapper_industry_properties and "read" in self._mapper_industry_properties:
            real_info = []
            for key in info:
                if key in self._mapper_industry_properties["read"]:
                    real_info.append(self._mapper_industry_properties["read"][key])
            info_returned = self._industrial_client.read(real_info)
            # mapeamos de vuelta
            info_returned_mapped = {}
            for original_key, mapped_key in self._mapper_industry_properties["read"].items():
                if mapped_key["map"] in info_returned:
                    info_returned_mapped[original_key] = info_returned[mapped_key["map"]]
            return info_returned_mapped
        else:
            return self._industrial_client.read(info)
