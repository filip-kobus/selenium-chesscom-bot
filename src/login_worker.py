from PyQt5.QtCore import QObject, pyqtSignal, QRunnable
from src.bot import Bot

class WorkerSignals(QObject):
    finished = pyqtSignal(object)

class LoginWorker(QRunnable):

    def __init__(self, email, password):
        super().__init__()
        self.email = email
        self.password = password
        self.signals = WorkerSignals()

    def run(self):
        bot = Bot()
        bot.open_page()
        bot.log_in(self.email, self.password)
        self.signals.finished.emit(bot)

