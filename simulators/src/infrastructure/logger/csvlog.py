import os
from src.domain.ilogger import ILogger
import csv


class CSVLog(ILogger):

    def __init__(self, params: dict):
        self._file_path = params['file_path']
        self._delimiter = params.get('delimiter', ',')
        self._print_headers = False
        self._file = None
        self._csv_writter = None

    def __del__(self):
        if self._file:
            self._file.close()

    def _init_writer(self, headers):
        if not os.path.exists(self._file_path):
            self._print_headers = True
        self._file = open(self._file_path, 'w+', encoding='utf-8', newline='')
        self._csv_writter = csv.DictWriter(self._file, delimiter=self._delimiter, fieldnames=headers)
        if self._print_headers:
            self._csv_writter.writeheader()

    def to_log(self, msg: dict):
        if self._csv_writter is None:
            self._init_writer(msg.keys())
        self._csv_writter.writerow(msg)
