from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from copy import deepcopy
from simple_term_menu import TerminalMenu
from src.domain.buggable import Bug, Buggable
from src.domain.utils import clear_terminal, check_for_numeric, check_date_time, datetime_now
import os
import time
import json
from datetime import datetime
import pandas as pd
from collections import defaultdict


targets = ["brandy", "brandyvalve", "conveyorbelt1", "coughsyrup", "coughsyrupvalve", "drain", "gin", "ginvalve", "mintcream", "mintcreamvalve", "mixtank1", "mixtank1valve", "mixtank2", "mixtank2valve", "peppermint", "peppermintvalve", "recolector", "recolectorvalve", "tequila", "tequilavalve"]


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Anomaly(Bug, metaclass=Singleton):

    anomaly_var_names = ["id", "target", "variable", "duration", "variance", "wander_factor", "type", "cutoff_value", "deployment_time", "periodicity", "ready"]
    anomaly_defaults = ["", None, "", 0, 0, 0, "", "", datetime_now().strftime("%Y-%m-%d %H:%M:%S"), 0, True]

    def reset(self):
        vars_copy = deepcopy(self.anomaly_var_names)

        for ndx, var in enumerate(vars_copy):
            if ndx != 1:
                setattr(self, var, self.anomaly_defaults[ndx])
                pass

    def get_dict_for_object(self):
        ret = {key: val for key, val in self.__dict__.items() if key in self.anomaly_var_names}
        return ret

    def set_values_from_existing_anomaly(self, bug: Bug):
        for var_name in self.anomaly_var_names:
            setattr(self, var_name, bug.__dict__[var_name])


class State(ABC):

    _cli = None

    @property
    def cli(self) -> Cli:
        return self._cli

    @property
    def name(self) -> None:
        return self._name

    @cli.setter
    def cli(self, cli: Cli) -> None:
        self._cli = cli

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @abstractmethod
    def run_pre(self) -> None:
        pass


class DeadEndState(State):

    @abstractmethod
    def do_something(self, str: str) -> None:
        pass


class DevicesMenu(State):

    options = targets + ["", "Back"]
    parent = None
    states = []

    def run_pre(self) -> None:
        clear_terminal()
        print("Devices:")


class DeviceMenu(State):

    options = ["Schedule new", "See all", "Back"]
    parent = DevicesMenu
    states = [None, None, parent]

    def run_pre(self) -> None:
        clear_terminal()
        if self.name in targets:
            print(self.name)
            setattr(SeeAll, 'devices', [self.name])
            setattr(Anomaly, 'target', self.name)


class UpdateAnomalyAtt(DeadEndState):

    options = [None]
    states = [None]

    def do_something(self, att_name: str):
        new_val = input(f"{att_name} (current={getattr(Anomaly, att_name)}, empty to exit): ")
        if new_val != "":
            if att_name in ["duration", "variance", "wander_factor", "periodicity"]:
                new_val = check_for_numeric(new_val)
            elif att_name in ['ready']:
                new_val = True if new_val.lower() == 'true' else False
            elif att_name in ['deployment_time']:
                valid_datetime = check_date_time(new_val)
                if not valid_datetime:
                    new_val = getattr(Anomaly, att_name)
                    print("Invalid datetime. Reverting to previous value. Please follow the formatting provided.")
                    input("Press 'Enter' to continue.")
            setattr(Anomaly, att_name, new_val)
        clear_terminal()


class ShowHelp(DeadEndState):

    options = [None]
    states = [None]

    def do_something(self, name: str):
        clear_terminal()
        cli = Cli()
        print("This is a help message at", name)
        input("Press 'Enter' to continue")
        clear_terminal()
        cli.setCli(DeviceMenu, "")
        pass


class SendAnomalyToBackend(DeadEndState):

    options = [None]
    states = [None]

    @staticmethod
    def calculate_deployment_time(anomaly):
        date_time = anomaly.deployment_time
        deployment_date = check_date_time(date_time)

        if deployment_date is None:
            input(f"Deployment time '{date_time} could no be processed.\nPress 'Enter' to return to the Scheduling menu.")
            return False
        else:
            return True

    def do_something(self, option_name: str):
        anomaly = Bug(Anomaly.get_dict_for_object(Anomaly))
        deployment_succeeded = self.calculate_deployment_time(anomaly)
        cli = Cli(self)
        if deployment_succeeded:
            cli.getBackend().schedule(anomaly)
            print("Anomaly scheduled...")
            time.sleep(3)
            cli.setCli(DeviceMenu, "")
        else:
            cli.setCli(ScheduleNew, "")
        clear_terminal()


class ScheduleNew(State):

    options = ["id", "target", "variable", "duration", "variance", "wander_factor", "type", "cutoff_value", "deployment_time", "ready", "", "help", "finish", "Back"]
    parent = DeviceMenu
    states = [UpdateAnomalyAtt, UpdateAnomalyAtt, UpdateAnomalyAtt, UpdateAnomalyAtt, UpdateAnomalyAtt, UpdateAnomalyAtt, UpdateAnomalyAtt, UpdateAnomalyAtt, UpdateAnomalyAtt, UpdateAnomalyAtt, None, ShowHelp, SendAnomalyToBackend, parent]

    def run_pre(self) -> None:
        print("Scheduled anomaly:")


class SeeAll(State):

    options = []
    states = None
    devices = copy.deepcopy(targets)

    def run_pre(self) -> None:
        clear_terminal()
        cli = Cli(self)
        scheduled_anomalies = cli.getBackend().get_scheduled_bugs
        anomalies_list = []

        for id, anomaly in scheduled_anomalies.items():
            if anomaly['target'] in self.devices:
                anomalies_list.append(anomaly)

        df = pd.DataFrame.from_dict(dict(self._merge_dict_for_display(anomalies_list)))
        if df.empty:
            print('Nothing scheduled.')
        else:
            print("All scheduled:")
            print(df.to_string(index=False))

        input("Press 'Enter' to continue")
        if self.devices == targets:
            parent = MainMenu
        else:
            parent = DeviceMenu
        devices = copy.deepcopy(targets)
        clear_terminal()
        cli.setCli(state=parent, name="")

    def _merge_dict_for_display(anomalies: list) -> defaultdict:
        merged_dict = defaultdict(list)

        for d in anomalies:
            for key, value in d.items():
                merged_dict[key].append(value)

        return merged_dict


class RequestId(State):

    options = None
    states = None

    def run_pre(self) -> None:
        bug = Anomaly()
        bug.reset()
        # cli = Cli(self)
        anomaly_id = ""
        while anomaly_id == "":
            anomaly_id = input("New or existing id: ")
        if anomaly_id in self.cli.backend.get_scheduled_bugs:
            a = self.cli.backend.get_scheduled_bugs[anomaly_id]
            bug = Bug(a)
            Anomaly.set_values_from_existing_anomaly(Anomaly, bug)
        else:
            setattr(Anomaly, 'id', anomaly_id)

        self.cli.setCli(ScheduleNew, "")
        clear_terminal()


class Exit(State):

    options = []
    parent = None

    def run_pre(self) -> None:
        exit()


class MainMenu(State):

    options = ["Devices", "See All Scheduled", "Exit"]
    states = [DevicesMenu, SeeAll, Exit]

    def run_pre(self) -> None:
        clear_terminal()
        print("Buggable CLI")
        setattr(SeeAll, 'devices', targets)


class Cli(metaclass=Singleton):

    _state = None
    options = []
    backend = None

    def __init__(self, state: State = MainMenu, targets_param=[], backend=Buggable) -> None:
        self.name = ""
        self.setCli(state)
        self.backend = backend if backend is not None else Buggable(targets=targets_param)
        # global targets
        # targets = targets_param

    def setCli(self, state: State, name: str = ""):
        self._state = state
        self._state.name = name
        self.options = state.options
        self._state.cli = self

    def getBackend(self):
        return self.backend

    def setup(self):
        clear_terminal()
        # DevicesMenu
        setattr(DevicesMenu, 'parent', MainMenu)
        setattr(DevicesMenu, 'states', [DeviceMenu] * len(targets) + ["", MainMenu])
        # DeviceMenu
        setattr(DeviceMenu, 'states', [RequestId, SeeAll, DevicesMenu])
        # UpdateBugAtt
        setattr(UpdateAnomalyAtt, 'parent', ScheduleNew)
        setattr(UpdateAnomalyAtt, 'states', [ScheduleNew])
        # Anomaly
        Anomaly.reset(Anomaly)
        # SeeAll
        setattr(SeeAll, 'states', [MainMenu, DeviceMenu])


    def run(self):
        self.setup()
        while True:
            self._state.run_pre(self._state)
            terminal_menu = TerminalMenu(self._state.options, skip_empty_entries=True)  # TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            next_state = self._state.states[menu_entry_index]
            if issubclass(next_state, DeadEndState):
                next_state.do_something(next_state, self.options[menu_entry_index])
            else:
                self.setCli(self._state.states[menu_entry_index], self.options[menu_entry_index])


def main():
    cli = Cli()
    cli.run()


if __name__ == "__main__":
    main()
