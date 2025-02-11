import sys, os, json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bot import Bot
import threading
from engine import engine
from time import sleep
from random import randint
import win32.lib.win32con as win32con
import win32gui
from app import Ui_MainWindow

class MainWindow:
    change_text = pyqtSignal(str)
    USER_FILE="config/user.json"
    SETTINGS = "config/settings.json"
    ICON = "config/icon.ico"

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.main_win.setWindowIcon(QIcon(self.ICON))
        self.ui.setupUi(self.main_win)
        self.ui.LoginButton.clicked.connect(lambda: self.login())
        self.ui.startButton.clicked.connect(lambda: self.start_bot())
        self.ui.auto_login.clicked.connect(lambda: self.open_login_page())
        self.ui.manual_login.clicked.connect(lambda: self.manual_login())
        self.ui.stop.clicked.connect(lambda: self.stop())
        self.ui.stackedWidget.setCurrentWidget(self.ui.ChoosePage)
        self.ui.remember.setChecked(self.check_if_remeber())
        self.load_settings()
        self.configure_sliders()
        self.bot = None

    def load_settings(self):
        with open(self.SETTINGS, 'r') as f:
            settings = json.load(f)

        self.ui.Rstockfishlevelcheck.setChecked(bool(settings["Rstockfishlevelcheck"]))
        self.ui.Rmovesaheadcheck.setChecked(bool(settings["Rmovesaheadcheck"]))
        self.ui.AutoMove.setChecked(bool(settings["AutoMove"]))
        self.ui.RThinkingTime.setChecked(bool(settings["RThinkingTime"]))

        self.ui.StockFishlevel.setSliderPosition(int(settings["StockFishlevel"]))
        self.ui.levelLabel.setText(str(settings["StockFishlevel"]))
        self.ui.MovesAhead.setSliderPosition(int(settings["MovesAhead"]))
        self.ui.movesLabel.setText(str(settings["MovesAhead"]))

        self.ui.RSLFROM.setValue(int(settings["RSLFROM"]))
        self.ui.RSLTO.setValue(int(settings["RSLTO"]))
        self.ui.RMAFROM.setValue(int(settings["RMAFROM"]))
        self.ui.RMATO.setValue(int(settings["RMATO"]))
        self.ui.thinkingTime.setSliderPosition(int(settings["thinkingTime"]))
        self.ui.thinkingLabel.setText(str(settings["thinkingTime"]))

    def configure_sliders(self):
        self.ui.MovesAhead.valueChanged['int'].connect(self.ui.movesLabel.setNum)
        self.ui.StockFishlevel.valueChanged['int'].connect(self.ui.levelLabel.setNum)
        self.ui.thinkingTime.valueChanged['int'].connect(self.ui.thinkingLabel.setNum)

    def save_settings(self):
        if self.ui.whiteButton.isChecked():
            color = "White"
        else:
            color = "Black"
        
        settings = {
            "Rstockfishlevelcheck": self.ui.Rstockfishlevelcheck.isChecked(),
            "Rmovesaheadcheck": self.ui.Rmovesaheadcheck.isChecked(),
            "AutoMove": self.ui.AutoMove.isChecked(),
            "RThinkingTime": self.ui.RThinkingTime.isChecked(),
            "StockFishlevel": self.ui.StockFishlevel.value(),
            "MovesAhead": self.ui.MovesAhead.value(),
            "RSLFROM": self.ui.RSLFROM.value(),
            "RSLTO": self.ui.RSLTO.value(),
            "RMAFROM": self.ui.RMAFROM.value(),
            "RMATO": self.ui.RMATO.value(),
            "thinkingTime": self.ui.thinkingTime.value(),
            "color": color
        }

        with open(self.SETTINGS, 'w') as f:
            json.dump(settings, f, indent=4)

        return settings

    def start_bot(self):
        settings = self.save_settings()
        status = self.bot.is_bot_or_live()
        if status is None:
            eGame = QMessageBox()
            eGame.setIcon(QMessageBox.Information)
            eGame.about(self.ui.stackedWidget, "ERROR", "You are not in game, start the game to run bot")
            return None
        color = settings['color']
        self.ui.stackedWidget.setCurrentWidget(self.ui.GamePage)
        self.worker = Worker(status, color, settings)
        self.worker.start()
        self.worker.move.connect(self.move)
        self.worker.end.connect(self.SettingsPage)
        self.worker.timeToMove.connect(self.timeToMove)
        self.worker.clear.connect(self.timeToMove)

    def show_move(self, move):
        self.ui.moveLabel.setText(move)

    def stop(self):
        with open('config/end.txt', 'w')  as f:
            f.write("end")

    def show_time_to_move(self, time):
        if time == "True":
            self.ui.timeLabel.setText("")
        else:
            self.ui.timeToMove.setText(str(time)+" s")

    def back_to_settings_page(self):
        self.ui.BestMove.setText("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.SettingsPage)

    def open_login_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.LoginPage)

    def login(self):
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
        self.t1 = threading.Thread(target=self.initialize_bot, args=[email, password], daemon=True)
        self.t1.start()

    def manual_login(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.LoadingPage)
        self.t1 = threading.Thread(target=self.initialize_bot, args=["", ""], daemon=True)
        self.t1.start()

    def initialize_bot(self, email, password):
        self.bot = Bot(email=email, password=password)
        self.bot.log_in()
        self.ui.stackedWidget.setCurrentWidget(self.ui.SettingsPage)

    def check_if_remeber(self):
        with open(self.USER_FILE, 'r') as f:
            user_data = json.load(f)
        if user_data.get("remember", False): 
            self.ui.email.setText(user_data["email"])
            self.ui.password.setText(user_data["password"])
            return True
        return False

    def show(self):
        self.main_win.show()

class Worker(QThread):
    move = pyqtSignal(str)
    end = pyqtSignal(bool)
    timeToMove = pyqtSignal(int)
    clear = pyqtSignal(str)

    def __init__(self, mode, color, settings):
        super().__init__()
        self.settings = settings
        self.mode = mode
        self.color = color
        self.isRSL = settings["Rstockfishlevelcheck"]
        self.isRMA = settings["Rmovesaheadcheck"]
        self.isautomves = settings["AutoMove"]
        self.isRTT = settings["RThinkingTime"]
        self.stockfishlevel = settings["Rstockfishlevelcheck"]
        self.movesahead = settings["MovesAhead"]
        self.thinkingtime = settings["thinkingTime"]
        self.running = True
        self.engine = None


    def run(self):
        try:
            self.engine = engine(self.stockfishlevel, self.movesahead)
            self.engine.clearBoard()
            try:
                moves = bot.movesBeforeLaunch()
                self.engine.setPosition(moves)
            except:
                bot.pickFigurine(self.mode)
                e.clearBoard()
                sleep(1)
                moves = bot.movesBeforeLaunch()
                e.setPosition(moves)

            while bot.checkIfGameEnd() is True and readFile() is False:
                var = 0
                
                if bot.whiteOrBlackMove(self.color  ) is True:
                    while True:
                        if var < 1:
                            var += 1
                            if bot.getPosition() is None:
                                if self.isRSL == "True" or self.isRMA == "True":
                                    e = self.setArgs(self.isRSL, self.isRMA)
                                move = e.firstMove()
                                if self.isautomves == "True":
                                    self.delay(self.isRTT, self.thinkingtime, move)
                                    bot.Move(move, self.color, self.mode)
                                    e.getData()
                                else:
                                    self.move.emit(move)
                            else:
                                if self.isRSL == "True" or self.isRMA == "True":
                                    e = self.setArgs(self.isRSL, self.isRMA)
                                try:
                                    move = e.BestMove(bot.getPosition())
                                except:
                                    print(Exception)
                                    bot.pickFigurine(self.mode)
                                    sleep(1)
                                    move = e.BestMove(bot.getPosition())
                                if self.isautomves == "True":
                                    self.delay(self.isRTT, self.thinkingtime, move)
                                    bot.Move(move, self.color, self.mode)
                                    e.getData()
                                else:
                                    self.move.emit(move)
                                    e.getData()
                        if bot.checkIfGameEnd() is False or readFile() is True :
                            break
                        if bot.whiteOrBlackMove(self.color) is False:
                            try:
                                e.BestMove(bot.getPosition())
                            except:
                                print(Exception)
                                bot.pickFigurine(self.mode)
                                sleep(1)
                                e.BestMove(bot.getPosition())
                            break
            self.end.emit(True)
        except Exception as exe:
            print(exe)
            self.end.emit(True)

    def stop(self):
        self.running = False
        self.wait()

    def randomInt(self, v1, v2):
        if v1 > v2:
            return randint(v2, v1)
        elif v1 < v2:
            return  randint(v1, v2)
        else:
            return v1

    def setOrRandom(self, level, isRandom, randomVal):
        if isRandom == "True":
            return randomVal
        else:
            return level

    def thinkingTime(self, value, isRandom):
        if isRandom == "True":
            return randint(1, value)
        else:
            return  value

    def delay(self, isRandom, time, move):
        if isRandom == "True":
            x = randint(0, time)
        else:
            x = time
        if x == 1:
            self.move.emit(move)
            self.timeToMove.emit(1)
            sleep(1)
        elif x == 0:
            self.move.emit(move)
        for i in range(x-1):
            if i == 0:
                self.move.emit(move)
            self.timeToMove.emit(x-i-1)
            sleep(1)
        self.clear.emit("True")

    def setArgs(self, isRSL, isRMA):
        self.randomstockfishlevel = self.randomInt(self.settings[6], self.settings[7])
        self.randommovesahead = self.randomInt(self.settings[8], self.settings[9])
        if isRSL == "True" and isRMA == "False":
            return engine(self.randomstockfishlevel, self.movesahead)

        elif isRSL == "False" and isRMA == "True":
            return engine(self.stockfishlevel, self.randommovesahead)

        elif isRSL == "True" and isRMA == "True":
            return engine(self.randomstockfishlevel, self.randommovesahead)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

