from stockfish import Stockfish
import chess

class Engine:
    STOCKFISH_PATH="config\stockfish.exe"
    def __init__(self, stockfish_level=20, moves_ahead=12):
        self.stockfish = Stockfish(self.STOCKFISH_PATH, parameters={'Move Overhead':stockfish_level, "Skill Level": moves_ahead})

    def get_best_move(self, fen):
        self.stockfish.set_fen_position(fen)
        move = self.stockfish.get_best_move_time(1000)
        return move

    def get_parameters(self):
        print(self.stockfish.get_parameters())

    def whose_move_is(self, fen):
        board = chess.Board(fen)
        return "White" if board.turn == chess.WHITE else "Black"

if __name__ == "__main__":
    pass
