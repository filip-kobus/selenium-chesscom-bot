from stockfish import Stockfish
import chess

class Engine:
    STOCKFISH_PATH="config\stockfish.exe"
    def __init__(self, stockfish_level=20):
        self.stockfish = Stockfish(self.STOCKFISH_PATH, parameters={"Skill Level": stockfish_level})
        self.board = chess.Board()

    def load_board(self, fen):
        self.board.set_fen(fen)

    def push_move(self, move):
        move_obj = chess.Move.from_uci(move)
        self.board.push(move_obj)

    def is_move_possible(self, move):
        try:
            move_obj = chess.Move.from_uci(move)
            return move_obj in self.board.legal_moves
        except ValueError:
            return False

    def get_best_move(self):
        fen = self.board.fen()
        self.stockfish.set_fen_position(fen)
        move = self.stockfish.get_best_move()
        return move

    def change_parameters(self, stockfish_level):
        self.stockfish.update_engine_parameters({
            'Skill Level': stockfish_level
        })

    def whose_move_is(self):
        return "w" if self.board.turn == chess.WHITE else "b"

if __name__ == "__main__":
    pass
