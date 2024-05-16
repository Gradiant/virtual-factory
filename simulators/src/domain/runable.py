from abc import abstractmethod
from threading import Thread
from time import sleep


class RunAble:

    def __init__(self):
        self._thread = Thread(target=self._run, daemon=True)
        self._running = False

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False

    def join(self):
        self._thread.join()

    def get_thread(self):
        return self._thread

    @abstractmethod
    def run_thread(self):
        raise NotImplemented

    def _run(self):
        while self._running:
            try:
                self.run_thread()
                sleep(1)
            except KeyboardInterrupt:
                self._running = False