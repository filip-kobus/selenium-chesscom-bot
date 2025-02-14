from PyQt5.QtCore import *
from engine import Engine

class Worker(QThread):
    move_signal = pyqtSignal(str)
    end_signal = pyqtSignal(bool)
    timeToMove_signal = pyqtSignal(int)
    update_settings_signal = pyqtSignal(int)

    def __init__(self, bot, settings):
        super().__init__()
        self.running = True
        self.engine = None
        self.bot = bot
        self.update_settings_signal.connect(self.update_settings)
        self.load_settings(settings)

    def load_settings(self, settings):
        self.settings = settings
        self.color = settings.get("color", "White")
        self.isRSL = settings.get("Rstockfishlevelcheck", False)
        self.isRMA = settings.get("Rmovesaheadcheck", False)
        self.isautomves = settings.get("AutoMove", False)
        self.isRTT = settings.get("RThinkingTime", False)
        self.stockfishlevel = settings.get("StockFishlevel", 1)
        self.movesahead = settings.get("MovesAhead", 1)
        self.thinkingtime = settings.get("thinkingTime", 0)
        self.bot.set_my_color = self.color

    def update_settings(self, settings):
        self.load_settings(settings)

    def run(self):
        self.engine = Engine(self.stockfishlevel, self.movesahead)
        bot = self.bot
        fen = bot.get_fen_of_current_state()
        self.engine.load_board(fen)
        while not bot.has_game_ended():
            try:
                move = bot.has_anyone_moved()
            except Exception:
                fen = bot.get_fen_of_current_state()
                self.engine.load_board(fen)
                continue
            if move is not None:
                try:
                    self.engine.push_move(move)
                except ValueError:
                    fen = bot.get_fen_of_current_state()
                    self.engine.load_board(fen)
                if bot.current_color != self.color:
                    best_move = self.engine.get_best_move()
                    print(best_move)
                    self.move_signal.emit(best_move)

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