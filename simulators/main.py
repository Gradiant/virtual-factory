import argparse
from application.app import App
from src.application.configuration.load_configuration import LoadConfiguration

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser')

parser_run = subparsers.add_parser('run',
                                     help='running mode')
parser_run.add_argument('-c', '--configuration_file', action='store', type=str, required=True,
                          help='Configuration file to use')


def run(configuration_file):
    config = LoadConfiguration().parse_from_file(configuration_file)
    app = App(config)
    app.run()


if __name__ == "__main__":
    kwargs = vars(parser.parse_args())
    globals()[kwargs.pop('subparser')](**kwargs)