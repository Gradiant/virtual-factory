from threading import Thread
from time import sleep
from src.domain.bug import Bug

class Buggable:

    def __init__(self, params: dict):
        self._name = params.get("name")
        self._buggable = params.get("buggable")
        self._buggable_notifier = params.get("buggable_notifier_client", None)
        self._bug_active = False
        self._bug_threads = {}
        self._bugging_element = None
        if self._buggable:
            self._bugging_element = params.get("bugging_element", None)
            if self._bugging_element:
                self._buggable_notifier.subscribe(self._bugging_element.get_name(), self._bugging_element.callback_subscription)

    def create_bug(self):
        bug_dict = self._bugging_element.get_bug_params()
        while len(bug_dict) > 0:
            first_key = None
            for key, value in bug_dict.items():
                first_key = key
                break
            bug_params = bug_dict.pop(first_key)
            bug = Bug(bug_params)
            bug_thread = Thread(target=self._do_bug, args=(bug,), daemon=True)
            self._bug_threads.update({bug_params['id']: bug_thread})
            bug_thread.start()

    def _do_bug(self, bug: Bug):

        _sim_sleep_interval = 1
        if self._name == bug.get_target() and bug.get_variable() in self.__dict__.keys() and bug.get_type() is not None:
            # backup
            bug.set_original_value(self.__dict__[bug.get_variable()])

            while bug.get_duration() > 0:
                self.__dict__[bug.get_variable()] = bug.get_bug_value()
                bug.set_duration(bug.get_duration() - 1)
                self._bug_active = True
                sleep(_sim_sleep_interval)

            _duration = bug.get_duration()
            if _duration < 0:
                _duration = 0
            # restablecemos el valor que tenía
            self.__dict__[bug.get_variable()] = bug.get_original_value()

            _periodicity = bug.get_periodicity()
            if _periodicity > _duration:
                sleep((_periodicity - _duration) * _sim_sleep_interval)
                new_bug = Bug(bug.get_initial_params())
                bug_thread = Thread(target=self._do_bug, args=(new_bug,), daemon=True)
                self._bug_threads.update({bug.get_id(): bug_thread})
                bug_thread.start()
            else:
                self._bug_threads.pop(bug.get_id())
                self._bug_active = len(self._bug_threads) > 0
