import time

from src.infrastructure.SimulatorMQTTClient import SimulatorMQTTClient
from threading import Thread, Timer
import json
from src.domain.utils import check_date_time, datetime_now, deployment_time_to_format

class Bug():
    def __init__(self, params: dict = {}):
        self.id = params.get("id")
        self.target = params.get("target", "")
        self.variable = params.get("variable", "")
        self.duration = params.get("duration", 0)
        if self.duration < 0:
            self.duration = 0
        self.variance = params.get("variance", 0)
        self.wander_factor = params.get("wander_factor", 0)
        self.type = params.get("type", "")
        self.value = params.get("cutoff_value", "")
        self.deployment_time = params.get("deployment_time", 0)
        self.ready = True
        self.periodicity = params.get("periodicity", 0)


class Buggable():

    def __init__(self, params: dict = {}, targets: list = []):
        self._client = SimulatorMQTTClient(params)
        self._targets = params.get("targets", targets)
        self._bugs = {}
        self._threads = {}

    def schedule(self, bug: Bug):
        bug_params = bug.__dict__
        if bug_params['target'] in self._targets:
            deploy_time = check_date_time(bug_params['deployment_time'])
            if deploy_time is not None and (deploy_time - datetime_now()).total_seconds() >= 0:
                bug_params['deployment_time'] = deployment_time_to_format(deploy_time)
                self._bugs.update({bug_params['id']: bug_params})
                bug_id = bug_params['id']
                if bug_id in self._threads:
                    self._threads[bug_id].cancel()
                t = Timer((deploy_time - datetime_now()).total_seconds(), function=self.deploy_scheduled, args=(bug_params,))
                t.daemon = True
                self._threads.update({bug_id: t})
                t.start()
        else:
            raise KeyError

    @property
    def get_scheduled_bugs(self):
        return self._bugs

    def deploy_scheduled(self, bug_params):
        deployed = self.deploy_bug(bug_params)
        if deployed:
            self._bugs.pop(bug_params['id'])
        self._threads.pop(bug_params['id'])

    def deploy_bug(self, bug_params):
        ret = False
        if bug_params['ready']:
            self._client.send(f"{bug_params['target']}_bug", bug_params)
            ret = True
        return ret

    def from_json_file(self, path: str):
        with open(path, 'r') as file:
            bugs_dict = json.load(file)
        for id, values in bugs_dict.items():
            values.setdefault('id', id)
            bug = Bug(values)
            deploy_time = check_date_time(bug.deployment_time)
            if deploy_time is not None:
                bug.deployment_time = str(deploy_time)
                self.schedule(bug)
        print(f"Scheduled anomalies in {path}")
        time.sleep(3)
