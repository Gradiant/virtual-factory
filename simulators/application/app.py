from time import sleep
from typing import List

from src.domain.externalioelement import ExternalIOElement
from src.domain.iindustrialconnectorclient import IIndustrialConnectorClient
from src.domain.isimulatorconnectorclient import ISimulatorConnectorClient
from src.domain.process import Process
from src.domain.simulators.process_factory import ProcessFactory
from src.domain.simulators.simulator import Simulator
from src.domain.simulators.simulator_factory import SimulatorFactory
from src.infrastructure.industrial.industrial_client_connect_factory import IndustrialClientConnectFactory
from src.infrastructure.simulators_connection.simulator_client_connect_factory import \
    SimulatorClientConnectFactory
from src.domain.flowabletobeltelement import FlowableToBeltElement
from src.domain.externalbuggingelement import ExternalBuggingElement
from src.infrastructure.logger.logger_factory import LoggerFactory
from src.domain.ilogger import ILogger


class App:

    def __init__(self, config: dict):
        self._config = config
        if __debug__:
            print("DEBUG MODE")
        else:
            print("PROD MODE")

    def run(self):
        simulator_connector = self.get_simulator_connector_client()
        industrial_connector = self.get_industrial_connector_client()
        simulators = self.get_simulators(simulator_connector, industrial_connector)
        processes = self.get_processes(industrial_connector)

        for simulator in simulators:
            simulator.start()

        for process in processes:
            process.start()

        print("Started")
        active = True
        while active:
            try:
                sleep(1)
            except KeyboardInterrupt:
                print("Exiting")
                active = False
                for process in processes:
                    process.stop()
                for simulator in simulators:
                    simulator.stop()
                    simulator.join()
                for process in processes:
                    process.join()

    def get_simulators(self, simulator_connector_client: ISimulatorConnectorClient,
                       industrial_client: IIndustrialConnectorClient) -> List[Simulator]:
        simulators = []
        for name in self._config.get("simulator_names", []):
            simulators.append(self.get_simulator(name, simulator_connector_client, industrial_client))
        return simulators

    def get_simulator(self, name, simulator_connector_client,
                      industrial_conector_client: IIndustrialConnectorClient) -> Simulator:
        simulator_config = self._config.get(name)
        inputs_names = simulator_config.get("inputs", [])
        outputs_names = simulator_config.get("outputs", [])
        if simulator_config.get("type") == 'conveyorbelt':
            flowable_inputs = simulator_config.get("flowable_inputs")
            simulator_config['flowable_inputs'] = self.get_flowable_to_belt_elements(flowable_inputs)
        if simulator_config.get("buggable", False):
            simulator_config["bugging_element"] = self.get_bugging_element(name)
        simulator_config["name"] = name
        simulator_config["inputs"] = self.get_external_io_elements(inputs_names)
        simulator_config["outputs"] = self.get_external_io_elements(outputs_names)
        simulator_config["simulator_connector_client"] = simulator_connector_client
        simulator_config["buggable_notifier_client"] = simulator_connector_client
        simulator_config["industrial_connector_client"] = industrial_conector_client
        return SimulatorFactory.get_simulator(simulator_config)

    def get_processes(self, industrial_client: IIndustrialConnectorClient) -> List[Process]:
        processes = []
        for name in self._config.get("processes_names", []):
            processes.append(self.get_process(name, industrial_client))
        return processes

    def get_process(self, name, industrial_conector_client: IIndustrialConnectorClient) -> Process:
        process_config = self._config.get(name)
        process_config["name"] = name
        process_config["industrial_connector_client"] = industrial_conector_client
        return ProcessFactory.get_process(process_config)

    def get_simulator_connector_client(self) -> ISimulatorConnectorClient:
        return SimulatorClientConnectFactory.get_connector_client(self._config.get("simulator_connector_client", {}))

    def get_industrial_connector_client(self) -> IIndustrialConnectorClient:
        return IndustrialClientConnectFactory.get_connector_client(self._config["industrial_connector_client"])

    @staticmethod
    def get_external_io_elements(name_list: List[str]) -> List[ExternalIOElement]:
        elements = []
        for _name in name_list:
            elements.append(ExternalIOElement(_name))
        return elements

    @staticmethod
    def get_bugging_element(target_name) -> ExternalBuggingElement:
        bugging_element = ExternalBuggingElement(target_name)
        return bugging_element

    @staticmethod
    def get_flowable_to_belt_elements(element_list: List[str]) -> dict:
        elements = {}
        for _name, _element_params in element_list.items():
            elements[_name] = FlowableToBeltElement(_name, _element_params)
        return elements

    @staticmethod
    def get_logger_element(params) -> ILogger:
        return LoggerFactory.get_logger(params)
