from PyQt5.QtCore import QObject, pyqtSignal, QRunnable
from bot import Bot

class WorkerSignals(QObject):
    finished = pyqtSignal(object)

class LoginWorker(QRunnable):

    def __init__(self, email="", password="", auto_login=True):
        super().__init__()
        self.email = email
        self.password = password
        self.is_autologin = auto_login
        self.signals = WorkerSignals()

    def run(self):
        bot = Bot(email=self.email, password=self.password)
        if self.is_autologin:
            bot.log_in()
        self.signals.finished.emit(bot)

