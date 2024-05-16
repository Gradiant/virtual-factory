import json
import re


class LoadConfiguration:

    def parse_from_file(self, file_path: str) -> dict:
        self.conf = {}
        with open(file_path, 'r') as config_file:
            self.conf = json.load(config_file)
        self._resolve_dict(self.conf)
        return self.conf

    def parse_from_str(self, json_str: str) -> dict:
        self.conf = json.loads(json_str)
        self._resolve_dict(self.conf)
        return self.conf

    def _resolve_dict(self, dictionary: dict):
        for key, value in dictionary.items():
            if isinstance(value, str):
                dictionary[key] = self._resolve_string(value)
            elif isinstance(value, dict):
                self._resolve_dict(value)
            elif isinstance(value, list):
                self._resolve_list(value)

    def _resolve_list(self, array: list):
        for i in range(0, len(array)):
            if isinstance(array[i], str):
                array[i] = self._resolve_string(array[i])
            elif isinstance(array[i], dict):
                self._resolve_dict(array[i])
            elif isinstance(array[i], list):
                self._resolve_list(array[i])

    def _resolve_string(self, value: str):
        if re.match(r'^\$\{.*\}$', value):
            # try environment value
            environment = re.findall(r'^\$\{ENV\.(.*?)\}$', value)
            if len(environment) == 1:
                return os.getenv(environment[0])
            else:
                # try object value
                objects_ref = re.findall(r'^\$\{(.*?)\}$', value)
                if len(objects_ref) == 1:
                    splits = objects_ref[0].split(".")
                    temp = self.conf
                    for split in splits:
                        temp = temp[split]
                    return temp
        return value
