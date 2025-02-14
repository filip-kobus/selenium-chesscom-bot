from stockfish import Stockfish
import chess

class Engine:
    STOCKFISH_PATH="config\stockfish.exe"
    def __init__(self, stockfish_level=20, moves_ahead=12):
        self.stockfish = Stockfish(self.STOCKFISH_PATH, parameters={'Move Overhead':stockfish_level, "Skill Level": moves_ahead})
        self.board = chess.Board()

    def load_board(self, fen):
        self.board.set_fen(fen)

    def push_move(self, move):
        move_obj = chess.Move.from_uci(move)
        self.board.push(move_obj)


    def get_best_move(self):
        fen = self.board.fen()
        self.stockfish.set_fen_position(fen)
        move = self.stockfish.get_best_move_time(300)
        return move

    def get_parameters(self):
        print(self.stockfish.get_parameters())

if __name__ == "__main__":
    pass
