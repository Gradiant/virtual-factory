import docker
from threading import Thread, Event
import csv
import logger.utils as utils
from os import makedirs, chmod, getenv
from time import sleep


directory = ""
project = ""
interval = 0
one_shot = False


def init_file_with_permission(filename: str):
    with open(filename, 'w'):
        pass
    chmod(filename, 0o644)


def sleep_log_interval():
    global interval
    global one_shot
    # -1 second to account for the API's minimum delay, -1 more second if one_shot is enabled.
    #  Calculating running average would be ideal
    sleep_interval = max(0, interval - 1 - int(one_shot))
    sleep(sleep_interval)


def log_summary(container, client):
    failure_event = Event()
    log_file_path = f'{directory}/{container}_stats.csv'
    global one_shot
    one_shot = False

    init_file_with_permission(log_file_path)

    with open(log_file_path, 'a') as stats_file:
        stats_file.write("datetime;container_name;CPU%;MEM usage;MEM %;NET IN;NET OUT;BLOCK IN;BLOCK OUT\n")
        while not failure_event.is_set():
            stats = api_call(client, container, failure_event)
            datetime = stats['read'].split(".")[0]
            block_in, block_out = utils.block_io(stats)
            net_in, net_out = utils.network_io(stats)
            stats_file.write(f"{datetime};{container};{utils.calculateCPUPercentUnix(stats)};{stats['memory_stats']['usage']};{utils.calculate_memory_perc(stats)};{net_in};{net_out};{block_in};{block_out}\n")
            stats_file.flush()
            sleep_log_interval()


def log_raw(container, client):
    failure_event = Event()
    log_file_path = f'{directory}/{container}_stats.log'

    init_file_with_permission(log_file_path)

    with open(f'{directory}/{container}_stats.log', 'a') as stats_file:
        while not failure_event.is_set():
            stats = api_call(client, container, failure_event)
            stats_file.write(f"{stats}\n")
            stats_file.flush()
            sleep_log_interval()


def log_full_as_csv(container, client):
    failure_event = Event()
    log_file_path = f'{directory}/{container}_stats.csv'

    init_file_with_permission(log_file_path)

    # TODO simplify column names after flattening
    sep = ";"
    with open(log_file_path, 'a') as stats_file:
        header_written = False
        while not failure_event.is_set():
            stats = api_call(client, container, failure_event)
            flattened_stats = utils.flatten(stats)
            if not header_written:
                csv_columns = flattened_stats.keys()
                writer = csv.DictWriter(stats_file, fieldnames=csv_columns, delimiter=sep, extrasaction='ignore')
                writer.writeheader()
                header_written = True
            writer.writerow(flattened_stats)
            stats_file.flush()
            sleep_log_interval()


def api_call(client, container_name_or_id, failure_event: Event):
    global one_shot
    reponse = {}
    api_call_params = {}
    if docker.__version__ > '6.0.1':
        api_call_params = {'container': container_name_or_id, 'decode': None, 'stream': False, 'one_shot': one_shot}
    else:
        api_call_params = {'container': container_name_or_id, 'decode': None, 'stream': False}
        
    try:
        reponse = client.api.stats(**api_call_params)
        if reponse['read'] == '0001-01-01T00:00:00Z':
            print(f"{container_name_or_id} returned most likely erroneous data. Exiting.", flush=True)
            failure_event.set()
    except Exception as e:
        print(e)
        failure_event.set()
    return reponse


def run(config: dict):
    client = docker.from_env()
    containers_all = client.containers.list()
    container_names = list()
    global directory
    global interval
    global one_shot
    global project
    includes = []
    excludes = []
    log_modes = {"summary": log_summary, "full": log_full_as_csv, "raw": log_raw}

    if config.get("config_file") is None:
        project = config.get("project_name", "")
        directory = config.get("directory", "./stats/")
        mode = config.get("mode", "full")
        interval = config.get("interval", 0)
        one_shot = bool(config.get("one-shot", 0))
        includes = config.get("include")
        excludes = config.get("exclude")
    if mode == 'summary':
        one_shot = False

    if project != "":
        directory = f'{directory}/{project}'
    makedirs(directory, exist_ok=True)

    if len(includes) == 1 and includes[0] == '':
        includes = [c.name for c in containers_all]

    [container_names.append(c.name) for c in containers_all if c.name.startswith(project) and c.name in includes and c.name not in excludes]
    if len(container_names) > 0:
        for containers in container_names:
            t = Thread(target=log_modes.get(mode, log_full_as_csv), args=[containers, client])
            t.start()
        print("Logging...")
    else:
        print("No containers found for the parameters given. Exiting..")
