from random import random

from src.domain.enums.bugtypeenum import BugTypeEnum


class Bug:

    def __init__(self, bug_params: dict):
        self._id = bug_params.get("id", None)
        self._initial_params = bug_params
        self._target = bug_params.get("target", None)
        self._variable = bug_params.get("variable", None)
        self._duration = bug_params.get("duration", 0)
        if self._duration < 0:
            self._duration = 0
        self._periodicity = bug_params.get('periodicity', 0)
        self._variance = bug_params.get("variance", 0)
        self._wander_factor = bug_params.get("wander_factor", 0)
        self._cutoff_value = bug_params.get("cutoff_value", 0)
        self._type = BugTypeEnum.get_by_str(bug_params.get("type", None))
        self._previous_value = None
        self._original_value = None

    def get_id(self):
        return self._id

    def get_target(self) -> str:
        return self._target

    def get_variable(self) -> str:
        return self._variable

    def set_duration(self, new_duration: int):
        self._duration = new_duration

    def get_duration(self) -> int:
        return self._duration

    def get_periodicity(self) -> int:
        return self._periodicity

    def get_type(self) -> BugTypeEnum:
        return self._type

    def get_original_value(self):
        return self._original_value

    def set_original_value(self, value):
        self._original_value = value
        self._previous_value = value

    def get_wander_factor(self) -> int:
        return self._wander_factor

    def _get_previous_value(self):
        return self._previous_value if self._previous_value is not None else self._original_value

    def get_variance(self) -> int:
        return self._variance

    def get_initial_params(self):
        return self._initial_params

    def get_bug_value(self):
        switch = {
            BugTypeEnum.noise: self._get_bug_noise_value,
            BugTypeEnum.wander: self._get_bug_wander,
            BugTypeEnum.zero_drop: self._get_bug_zero_drop,
            BugTypeEnum.cutoff: self._get_bug_cutoff,
        }
        if self.get_type() is not None:
            return switch[self.get_type()]()
        return self._original_value

    def _get_bug_noise_value(self):
        _noise_variance = ((random() - 0.5) * self.get_variance())
        return self._original_value + _noise_variance

    def _get_bug_zero_drop(self):
        return 0

    def _get_bug_wander(self):
        _value = self._get_previous_value() + self.get_wander_factor()
        self._previous_value = _value
        return _value

    def _get_bug_cutoff(self):
        return self._cutoff_value
