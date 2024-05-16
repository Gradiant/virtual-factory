from src.cli.cli import Cli
from src.domain.buggable import Buggable
from time import sleep
import argparse
import os


parser = argparse.ArgumentParser(description="Deploy anomalies to SYP-POC-fabrica-virtual.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--file", help="Path to json file with anomalies.")
parser.add_argument("-d", help="Start in detached mode (no cli). Usage of -f is then required to give functionality to the program.", action="store_true")

targets_param = ["brandy", "brandyvalve", "conveyorbelt1", "coughsyrup", "coughsyrupvalve", "drain", "gin", "ginvalve", "mintcream", "mintcreamvalve", "mixtank1", "mixtank1valve", "mixtank2", "mixtank2valve", "peppermint", "peppermintvalve", "recolector", "recolectorvalve", "tequila", "tequilavalve"]

broker = os.getenv("MQTT_BROKER", "localhost")

buggable = Buggable({'targets': targets_param, "host": broker})
args = vars(parser.parse_args())
if args.get('file', None) is not None:
    buggable.from_json_file(args.get("file"))

if args.get('d'):
    print(buggable.get_scheduled_bugs)
    print("Started in detached mode.")
    while len(buggable.get_scheduled_bugs) > 0:
        sleep(1)
else:
    cli = Cli(backend=buggable)
    cli.run()
