from PyQt5.QtCore import *
from engine import Engine
import random
from timer_worker import TimerWorker
import traceback

class WorkerSignals(QObject):
    move_signal = pyqtSignal(str)
    end_signal = pyqtSignal()
    terminate_signal = pyqtSignal()
    time_to_move_signal = pyqtSignal(int)
    crashed_signal = pyqtSignal()

class BotWorker(QThread):

    def __init__(self, bot, settings):
        super().__init__()
        self.running = True
        self.is_automove_pending = False
        self.bot = bot
        self.signals = WorkerSignals()
        self.timer_worker = None
        self.load_settings(settings)
        self.signals.terminate_signal.connect(self.stop)

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
            self.stop_timer()
            self.signals.crashed_signal.emit()
            error_message = traceback.format_exc()
            print(f"BOT CRASHED: {error_message}")
        finally:
            self.signals.end_signal.emit()

    def run_bot(self):
        self.engine = Engine(self.stockfishlevel, self.movesahead)
        self.initialize_bot()
        self.emit_time_to_move(-1)

        while not self.bot.has_game_ended():
            if not self.running:
                break

            if self.is_automove_pending:
                self.bot.make_move(self.best_move)
                self.is_automove_pending = False

            try:
                move = self.bot.has_anyone_moved()
            except ValueError:
                move = " "

            if move is not None:
                self.signals.move_signal.emit("...")
                self.stop_timer()
                
                if self.engine.is_move_possible(move):
                    self.engine.push_move(move)
                else:
                    self.update_board_state()

                color = self.engine.whose_move_is()
                
                if color == self.color :
                    if self.isRSL or self.isRMA:
                        self.change_engine_parameters()
                    self.make_move()
                else:
                    self.signals.move_signal.emit("...")
            QThread.msleep(100)

    def stop_timer(self):
        if self.timer_worker is not None:
            self.timer_worker.signals.countdown_stopped.emit()
            self.emit_time_to_move(-1)
            self.timer_worker = None

    def initialize_bot(self):
        self.update_board_state()
        color = self.engine.whose_move_is()
        self.signals.move_signal.emit("...")
        if color == self.color:
            self.make_move()
    
    def update_board_state(self):
        fen = self.bot.get_fen_of_current_state()
        self.engine.load_board(fen)

    def make_move(self):
        self.best_move = self.engine.get_best_move()
        self.signals.move_signal.emit(self.best_move)
        if self.isAutomove:
            self.start_timer()

    def start_timer(self):
        time_to_move = self.get_time_to_move()

        self.timer_worker = TimerWorker(time_to_move)
        self.timer_worker.signals.update_countdown.connect(self.emit_time_to_move)
        self.timer_worker.signals.countdown_finished.connect(self.on_countdown_finished)
        self.timer_worker.signals.automove_request.connect(self.on_automove_request)

        QThreadPool.globalInstance().start(self.timer_worker)

    def on_automove_request(self):
        self.is_automove_pending = True

    def change_engine_parameters(self):
        stockfish_level = self.get_stockfish_level()
        moves_overhead = self.get_moves_overhead() 
        self.engine.change_parameters(stockfish_level, moves_overhead)

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
    
    def get_time_to_move(self):
        time = self.thinkingtime
        if self.isRTT:
            time = random.randint(0, time)
        return time

    def emit_time_to_move(self, time):
        self.signals.time_to_move_signal.emit(time)

    def on_countdown_finished(self):
        self.timer_worker = None

    def get_bot(self):
        return self.bot

    def stop(self):
        self.running = False