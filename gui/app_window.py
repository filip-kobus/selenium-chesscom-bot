import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.bot import Bot
from gui.Ui_MainWindow import Ui_MainWindow
from src.bot_worker import BotWorker
from src.login_worker import LoginWorker

class MainWindow(QMainWindow):
    USER_FILE="config/user.json"
    SETTINGS = "config/settings.json"
    ICON = "config/icon.ico"

    def __init__(self):
        super().__init__()
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.main_win.setWindowIcon(QIcon(self.ICON))
        self.setWindowTitle("Chess Bot")
        self.ui.setupUi(self.main_win)
        self.connect_buttons()
        self.load_settings()
        self.configure_sliders()
        self.bot = None

    def connect_buttons(self):
        self.ui.LoginButton.clicked.connect(lambda: self.auto_login())
        self.ui.startButton.clicked.connect(lambda: self.start_bot())
        self.ui.auto_login.clicked.connect(lambda: self.open_auto_login_page())
        self.ui.manual_login.clicked.connect(lambda: self.manual_login())
        self.ui.stop.clicked.connect(lambda: self.stop())
        self.ui.stackedWidget.setCurrentWidget(self.ui.ChoosePage)
        self.ui.remember.setChecked(self.check_if_remeber())

    def load_settings(self):
        with open(self.SETTINGS, 'r') as f:
            settings = json.load(f)

        self.ui.Rstockfishlevelcheck.setChecked(bool(settings["Rstockfishlevelcheck"]))
        self.ui.AutoMove.setChecked(bool(settings["AutoMove"]))
        self.ui.Rthinkingtimecheck.setChecked(bool(settings["RThinkingTime"]))

        self.ui.StockFishlevel.setSliderPosition(int(settings["StockFishlevel"]))
        self.ui.levelLabel.setText(str(settings["StockFishlevel"]))

        self.ui.RSLFROM.setValue(int(settings["RSLFROM"]))
        self.ui.RSLTO.setValue(int(settings["RSLTO"]))
        self.ui.RTTFROM.setValue(int(settings["RTTFROM"]))
        self.ui.RTTTO.setValue(int(settings["RTTTO"]))
        self.ui.thinkingTime.setSliderPosition(int(settings["thinkingTime"]))
        self.ui.thinkingLabel.setText(str(settings["thinkingTime"]))

    def configure_sliders(self):
        self.ui.StockFishlevel.valueChanged['int'].connect(self.ui.levelLabel.setNum)
        self.ui.thinkingTime.valueChanged['int'].connect(self.ui.thinkingLabel.setNum)
        self.ui.moveLabel.setText("")
        self.ui.timeLabel.setText("")
        self.ui.password.setEchoMode(QLineEdit.Password)

    def open_auto_login_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.LoginPage)

    def auto_login(self):
        email = self.ui.email.text()
        password = self.ui.password.text()
        remember_me = self.ui.remember.isChecked()

        if remember_me:
            user_data = {
                "email": email,
                "password": password,
                "remember": True
            }

        else:
            user_data = {
                "email": "",
                "password": "",
                "remember": False
            }

        with open(self.USER_FILE, "w") as f:
            json.dump(user_data, f, indent=4)

        self.ui.stackedWidget.setCurrentWidget(self.ui.LoadingPage)
        worker = LoginWorker(email, password)
        worker.signals.finished.connect(self.on_logged_in)

        QThreadPool.globalInstance().start(worker)

    def on_logged_in(self, bot):
        self.bot = bot
        self.ui.stackedWidget.setCurrentWidget(self.ui.SettingsPage)

    def manual_login(self):
        self.bot = Bot()
        self.bot.open_page()
        self.ui.stackedWidget.setCurrentWidget(self.ui.SettingsPage)

    def check_if_remeber(self):
        with open(self.USER_FILE, 'r') as f:
            user_data = json.load(f)
        if user_data.get("remember", False): 
            self.ui.email.setText(user_data["email"])
            self.ui.password.setText(user_data["password"])
            return True
        return False

    def save_settings(self):
        settings = {
            "Rstockfishlevelcheck": self.ui.Rstockfishlevelcheck.isChecked(),
            "AutoMove": self.ui.AutoMove.isChecked(),
            "RThinkingTime": self.ui.Rthinkingtimecheck.isChecked(),
            "StockFishlevel": self.ui.StockFishlevel.value(),
            "RSLFROM": self.ui.RSLFROM.value(),
            "RSLTO": self.ui.RSLTO.value(),
            "RTTFROM": self.ui.RTTFROM.value(),
            "RTTTO": self.ui.RTTTO.value(),
            "thinkingTime": self.ui.thinkingTime.value()
        }

        with open(self.SETTINGS, 'w') as f:
            json.dump(settings, f, indent=4)

        return settings

    def start_bot(self):
        settings = self.save_settings()
        if not self.bot.is_in_game() or self.bot.is_game_over():
            self.not_in_game_exception()
            return
        self.ui.stackedWidget.setCurrentWidget(self.ui.GamePage)
        self.worker = BotWorker(self.bot, settings)
        self.worker.signals.move_signal.connect(self.show_move)
        self.worker.signals.end_signal.connect(self.back_to_settings_page)
        self.worker.signals.crashed_signal.connect(self.crashed_exception)
        self.worker.signals.time_to_move_signal.connect(self.show_time_to_move)
        self.worker.start()

    def crashed_exception(self):
        eGame = QMessageBox()
        eGame.setIcon(QMessageBox.Information)
        eGame.about(self.ui.stackedWidget, "ERROR", "Bot crashed, start again")

    def not_in_game_exception(self):
        eGame = QMessageBox()
        eGame.setIcon(QMessageBox.Information)
        eGame.about(self.ui.stackedWidget, "ERROR", "You are not in game, start the game to run bot")
        self.back_to_settings_page()
        
    def show_move(self, move):
        self.ui.moveLabel.setText(move)

    def show_time_to_move(self, time):
        if time > 0:
            self.ui.timeLabel.setText(f"{str(time)} s")
        else:
            self.ui.timeLabel.setText("")
            
    def back_to_settings_page(self):
        self.ui.moveLabel.setText("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.SettingsPage)

    def stop(self):
        self.worker.signals.terminate_signal.emit()

    def show(self):
        self.main_win.show()

if __name__ == '__main__':
    pass

