from PyQt5.QtCore import QObject, pyqtSignal, QRunnable
import time

class WorkerSignals(QObject):
    update_countdown = pyqtSignal(int)
    automove_request = pyqtSignal()
    countdown_stopped = pyqtSignal()
    countdown_finished = pyqtSignal()

class TimerWorker(QRunnable):
    def __init__(self, time):
        super().__init__()
        self.time = time
        self.signals = WorkerSignals()
        self.signals.countdown_stopped.connect(self.stop)
        self.running = True

    def run(self):
        for remaining in range(self.time, 0, -1):
            if not self.running:
                self.signals.countdown_finished.emit()
                return
            self.signals.update_countdown.emit(remaining)
            time.sleep(1)
        self.signals.countdown_finished.emit()
        self.signals.automove_request.emit()

    def stop(self):
        self.running = False
