from time import sleep
from datetime import datetime
import csv
from threading import Thread
from os import chmod
from src.domain.ilogger import ILogger


class Logger(ILogger):

    def __init__(self, filename, interval, directory):
        self._separator = ';'
        self._first_log = True
        self._object = None
        self._filename = f"{directory}{filename}"
        self._interval = interval
        self._thread = Thread(target=self.to_log, daemon=True)
        self._thread.start()

    def to_log(self):
        while self._object is None:
            sleep(1)
            pass
        with open(f'{self._filename}', 'w'):
            pass
        chmod(f'{self._filename}', 0o744)

        sep = self._separator
        log_data = self._object.dict_for_log()
        log_data.update({'time': 0})
        csv_columns = log_data.keys()

        with open(f'{self._filename}', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=sep, extrasaction='ignore')
            writer.writeheader()
            while True:
                date = datetime.now()
                date = date.replace(microsecond=0)
                log_data = {'time': date}
                log_data.update(self._object.dict_for_log())
                writer.writerow(log_data)
                csvfile.flush()
                sleep(self._interval)
