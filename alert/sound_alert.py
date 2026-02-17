import winsound
import threading
import time

class Alert:
    def __init__(self):
        self.active = False

    def start(self):
        if not self.active:
            self.active = True
            threading.Thread(target=self._beep_loop, daemon=True).start()

    def _beep_loop(self):
        while self.active:
            winsound.Beep(2500, 700)
            time.sleep(0.1)

    def stop(self):
        self.active = False
