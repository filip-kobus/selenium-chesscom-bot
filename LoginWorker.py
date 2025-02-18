class LoginWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, email, password, bot_holder):
        super().__init__()
        self.email = email
        self.password = password
        self.bot_holder = bot_holder

    def run(self):
        try:
            self.bot_holder["bot"] = Bot(email=self.email, password=self.password)
            self.bot_holder["bot"].log_in()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
