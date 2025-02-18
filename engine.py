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

    def is_move_possible(self, move):
        move_obj = chess.Move.from_uci(move)
        if move_obj in self.board.legal_moves:
            return True
        return False

    def get_best_move(self):
        fen = self.board.fen()
        self.stockfish.set_fen_position(fen)
        move = self.stockfish.get_best_move_time(500)
        return move

    def change_parameters(self, stockfish_level, move_overhead):
        self.stockfish.update_engine_parameters({
            'Skill Level': stockfish_level,
            'Move Overhead': move_overhead
        })

    def whose_move_is(self):
        return "w" if self.board.turn == chess.WHITE else "b"

if __name__ == "__main__":
    pass
