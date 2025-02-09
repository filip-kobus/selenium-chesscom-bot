from stockfish import Stockfish
import chess

board = chess.Board()

class engine:
    def __init__(self, SFLevel, MovesA):
        self.stockfish = Stockfish(r"config\stockfish.exe", parameters={'Move Overhead':MovesA, "Skill Level": SFLevel})

    def BestMove(self, San):
        board.push_san(San)
        self.stockfish.set_fen_position(board.fen())
        move = self.stockfish.get_best_move_time(1000)
        return move

    def firstMove(self):
        self.stockfish.set_position()
        move = self.stockfish.get_best_move_time(1000)
        return move

    def setPosition(self, moves):
        for i in range(len(moves)):
            board.push_san(moves[i])

    def getData(self):
        print(self.stockfish.get_parameters())

    def clearBoard(self):
        board.reset()

if __name__ == "__main__":
    pass
