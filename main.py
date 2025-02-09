import sys, os
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
from gui import Ui_MainWindow

the_program_to_hide = win32gui.GetForegroundWindow()            #if you want run console remove this line
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)     #and that

class MainWindow:
    change_text = pyqtSignal(str)

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.main_win.setWindowIcon(QIcon("config/icon.ico"))
        self.ui.setupUi(self.main_win)
        self.ui.LoginButton.clicked.connect(lambda: self.loginSession())
        self.ui.Start.clicked.connect(lambda: self.Launch())
        self.ui.StopButton.clicked.connect(lambda: self.stop())
        self.ui.stackedWidget.setCurrentWidget(self.ui.LoginPage)
        self.ui.Remember.setChecked(self.Remember())
        self.defSettings = self.settingsInput()

    def settingsInput(self):
        with open('config/settings.txt', 'r')  as f:
            lines = f.readlines()

        def extract(line):
            line = line.rstrip("\n")
            result = line.split("=")
            return result[1]

        self.ui.Rstockfishlevelcheck.setChecked(bool(extract(lines[0])))
        self.ui.Rmovesaheadcheck.setChecked(bool(extract(lines[1])))
        self.ui.AutoMove.setChecked(bool(extract(lines[2])))
        self.ui.RThinkingTime.setChecked(bool(extract(lines[3])))

        self.ui.StockFishlevel.setSliderPosition(int(extract(lines[4])))
        self.ui.levelLabel.setText(extract(lines[4]))
        self.ui.MovesAhead.setSliderPosition(int(extract(lines[5])))
        self.ui.movesLabel.setText(extract(lines[5]))
        self.ui.RSLFROM.setValue(int(extract(lines[6])))
        self.ui.RSLTO.setValue(int(extract(lines[7])))
        self.ui.RMAFROM.setValue(int(extract(lines[8])))
        self.ui.RMATO.setValue(int(extract(lines[9])))
        self.ui.thinkingTime.setSliderPosition(int(extract(lines[10])))
        self.ui.thinkingLabel.setText(extract(lines[10]))

    def settingsOutput(self):
        settings = []
        settings.append(str(self.ui.Rstockfishlevelcheck.isChecked()))
        settings.append(str(self.ui.Rmovesaheadcheck.isChecked()))
        settings.append(str(self.ui.AutoMove.isChecked()))
        settings.append(str(self.ui.RThinkingTime.isChecked()))

        settings.append(self.ui.StockFishlevel.value())
        settings.append(self.ui.MovesAhead.value())
        settings.append(self.ui.RSLFROM.value())
        settings.append(self.ui.RSLTO.value())
        settings.append(self.ui.RMAFROM.value())
        settings.append(self.ui.RMATO.value())
        settings.append(self.ui.thinkingTime.value())
        result = []
        for i in range(len(settings)):
            if settings[i] == "True":
                result.append('=n' + '\n')
            elif settings[i] == "False":
                result.append('=' + '\n')
            else:
                result.append('=' + str(settings[i]) + '\n')

        with open('config/settings.txt', 'w')  as f:
            f.writelines(result)
        return settings

    def Launch(self):
        settings = self.settingsOutput()
        open('config/end.txt', 'w').close()
        try:
            mode = bot.BotOrLive()
            if mode == "daily" or mode is None:
                eGame = QMessageBox()
                eGame.setIcon(QMessageBox.Information)
                eGame.about(self.ui.stackedWidget, "ERROR", "You are not in game, start the game to run BOT")
                return None
            colour = bot.BlackOrWhite()

        except:
            print(Exception)
            return None
        self.ui.stackedWidget.setCurrentWidget(self.ui.BotPage)
        self.worker = Worker(mode, colour, settings)
        self.worker.start()
        self.worker.move.connect(self.move)
        self.worker.end.connect(self.settingsPage)
        self.worker.timeToMove.connect(self.timeToMove)
        self.worker.clear.connect(self.timeToMove)

    def move(self, val):
        self.ui.BestMove.setText(val)

    def stop(self):
        with open('config/end.txt', 'w')  as f:
            f.write("end")

    def timeToMove(self, val):
        if val == "True":
            self.ui.timeToMove.setText("")
        else:
            self.ui.timeToMove.setText(str(val)+" s")

    def settingsPage(self, val):
        self.ui.BestMove.setText("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.SettingsPage)

    def loginSession(self):
        usr = self.ui.Username.text()
        passwd = self.ui.Password.text()
        if self.ui.Remember.isChecked() is False:
            open('config/data.txt', 'w').close()
        else:
            with open('config/data.txt', 'w')  as f:
                f.writelines([usr, "\n" + passwd, "\nremember"])

        self.ui.stackedWidget.setCurrentWidget(self.ui.LoadingPage)
        self.t1 = threading.Thread(target=self.openBot, args=[usr,passwd])
        self.t1.start()

    def openBot(self, usr, passwd):
        global bot
        bot = Bot(usr=usr, passwd=passwd)
        bot.openPage()
        self.ui.stackedWidget.setCurrentWidget(self.ui.SettingsPage)

    def Remember(self):
        with open('config/data.txt', 'r')  as f:
            data = f.readlines()
            if len(data) > 2:
                self.ui.Username.setText(data[0].rstrip("\n"))
                self.ui.Password.setText(data[1].rstrip("\n"))
                return True
            else:
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
        self.isRSL = settings[0]
        self.isRMA = settings[1]
        self.isautomves = settings[2]
        self.isRTT = settings[3]
        self.stockfishlevel = settings[4]
        self.movesahead = settings[5]
        self.thinkingtime = settings[10]


    def run(self):
        def readFile():
            filesize = os.path.getsize("config\end.txt")
            if filesize == 0:
                return False
            else:
                return True

        try:
            global e
            e = engine(self.stockfishlevel, self.movesahead)
            e.clearBoard()
            try:
                moves = bot.movesBeforeLaunch()
                e.setPosition(moves)
            except:
                bot.pickFigurine(self.mode)
                e.clearBoard()
                sleep(1)
                moves = bot.movesBeforeLaunch()
                e.setPosition(moves)

            while bot.checkIfGameEnd() is True and readFile() is False:
                var = 0
                if bot.whiteOrBlackMove(self.color) is True:
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

