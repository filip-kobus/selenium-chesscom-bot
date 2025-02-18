from PyQt5.QtCore import *
from engine import Engine
from time import sleep
import random

class Worker(QThread):
    move_signal = pyqtSignal(str)
    end_signal = pyqtSignal()
    terminate_signal = pyqtSignal()
    time_to_move_signal = pyqtSignal(int)
    not_in_game_signal = pyqtSignal()

    def __init__(self, bot, settings):
        super().__init__()
        self.running = True
        self.engine = None
        self.bot = bot
        self.terminate_signal.connect(self.stop)
        self.load_settings(settings)

    def load_settings(self, settings):
        self.settings = settings

        self.isRSL = settings.get("Rstockfishlevelcheck", False)
        self.isRMA = settings.get("Rmovesaheadcheck", False)
        self.isAutomove = settings.get("AutoMove", False)
        self.isRTT = settings.get("RThinkingTime", False)

        self.stockfishlevel = settings.get("StockFishlevel", 1)
        self.movesahead = settings.get("MovesAhead", 1)
        self.thinkingtime = settings.get("thinkingTime", 0)

        self.rsl_from = settings.get("RSLFROM", 1)
        self.rsl_to = settings.get("RSLTO", 20)
        self.rma_from = settings.get("RMAFROM", 1)
        self.rma_to = settings.get("RMATO", 20)

        self.color = settings.get("color", "w")
        self.bot.set_my_color(self.color)

    def run(self):
        try:
            self.run_bot()
        except Exception as e:
            print(e)
            self.not_in_game_signal.emit()
        finally:
            self.end_signal.emit()

    def run_bot(self):
        self.engine = Engine(self.stockfishlevel, self.movesahead)
        bot = self.bot
        fen = bot.get_fen_of_current_state()
        self.engine.load_board(fen)
        color = self.engine.whose_move_is()
        self.move_signal.emit("...")
        self.time_to_move_signal.emit(None)
        if color == self.color:
            best_move = self.engine.get_best_move()
            self.move_signal.emit(best_move)

        while self.running and not bot.has_game_ended():
            try:
                move = bot.has_anyone_moved()
            except Exception:
                fen = bot.get_fen_of_current_state()
                self.engine.load_board(fen)
                continue

            if move is not None:
                try:
                    if not self.engine.is_move_possible(move):
                        raise ValueError
                    self.engine.push_move(move)
                except ValueError:
                    fen = bot.get_fen_of_current_state()
                    self.engine.load_board(fen)

                color = self.engine.whose_move_is()
                
                if color == self.color :
                    if self.isAutomove:
                        self.auto_move(best_move)
                        continue
                    best_move = self.engine.get_best_move()
                    self.move_signal.emit(best_move)
                else:
                    self.move_signal.emit("...")

    def auto_move(self, move):
        time = self.get_time_to_move()
        if self.isRSL or self.isRMA:
            stockfish_level = self.get_stockfish_level()
            moves_overhead = self.get_moves_overhead() 
            self.engine.change_parameters(stockfish_level, moves_overhead)
        best_move = self.engine.get_best_move()
        self.move_signal.emit(best_move)
        self.emit_time_to_move(time)

    def get_time_to_move(self):
        time = self.thinkingtime
        if self.isRTT:
            time = random.randint(0, time)
        return time

    def get_stockfish_level(self):
        if self.isRSL:
            low, high = sorted((self.rsl_from, self.rsl_to))
            return random.randint(low, high)
        return self.stockfishlevel

    def get_moves_overhead(self):
        if self.isRMA:
            low, high = sorted((self.rma_from, self.rma_to))
            return random.randint(low, high)
        return self.movesahead
    
    def emit_time_to_move(self, time):
        time_to_end = time
        while time_to_end > 0 and self.running:
            self.time_to_move_signal.emit(time_to_end)
            sleep(1)
            time_to_end -= 1
        self.time_to_move_signal.emit(None)

    def stop(self):
        self.running = False
        self.wait()