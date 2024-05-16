import argparse
import os
from logger.logger import run
import yaml
from time import sleep
from distutils.util import strtobool

parser = argparse.ArgumentParser(description="Log Docker's system utilization.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--config_file", help="Path to yaml config file.")
parser.add_argument("-d", "--directory", help='Directory where log files will be stored.', default=os.getcwd() + "/stats")
parser.add_argument("-e", "--env", help='Get settings from environment variables.', action="store_true")
parser.add_argument("-ex", "--exclude", nargs='+', help="Names of containers to ignore, separated by commas", default="")
parser.add_argument("-i", "--interval", help="Interval between log entries in seconds. Due to the Docker API's response time it's impossible to get an interval time below 1 second.", default=0)
parser.add_argument("-in", "--include", nargs='+', help="Names of containers to monitor.", default="")
parser.add_argument("-m", "--mode", help='Archive mode. Options: summary, raw, full', default="full")
parser.add_argument("-o", "--one-shot", help="Improve response time, decreasing the interval between entries. Ignored when using 'summary' logging mode. See Docker API's documentation for more details: https://docs.docker.com/engine/api/v1.43/#tag/Container/operation/ContainerStats", default=True)
parser.add_argument("-p", "--project_name", help="Project name. Only containers whose name begins with the provided project name will be monitored. Otherwise, all containers will be monitored.", default="")
parser.add_argument("-w", "--wait", help="Seconds to wait before stating. Useful when running as part of a docker compose project to ensure all containers have started.", default=0)


if __name__ == "__main__":
    config = vars(parser.parse_args())
    config_file = config.get("config_file")
    if config_file is not None:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    elif config.get("env"):
        config["directory"] = os.getenv("LOGGING_DIRECTORY")
        config["project_name"] = os.getenv("DOCKER_PROJECT", "")
        try:
            config["interval"] = int(os.getenv("LOGGING_INTERVAL"))
        except ValueError:
            config["interval"] = 1
        config["mode"] = os.getenv("LOGGING_MODE")
        config["one-shot"] = strtobool(os.getenv("LOGGING_ONE_SHOT"))

        split_list = os.getenv("LOGGING_INCLUDE", "").split(",")
        includes = [name.strip() for name in split_list]
        config["include"] = includes

        split_list = os.getenv("LOGGING_EXCLUDE", "").split(",")
        excludes = [name.strip() for name in split_list]
        config["exclude"] = excludes
        
        config["wait"] = int(os.getenv("LOGGING_WAIT"), 0)
    sleep(config["wait"])
    print(config)
    run(config)
