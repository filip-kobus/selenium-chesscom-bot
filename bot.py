from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from engine import Engine
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import chromedriver_autoinstaller

import chess

class Bot:
    chromedriver_autoinstaller.install()
    PATH = "chromedriver.exe"
    URL = "https://www.chess.com/pl/login"

    def __init__(self, url=URL, password="", email="", player_color="w"):
        self.password = password
        self.email = email
        self.url = url
        self.driver = webdriver.Chrome(self.PATH)
        self.card = self.driver.get(self.url)
        self.driver.maximize_window()
        self.previous_pieces = set()
        self.current_pieces = set()
        self.castling_availability_fen = "KQkq"
        self.my_color = player_color

    def log_in(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(self.email)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(self.password)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))).click()
        except Exception:
            print("Unable to log in. Do it manually.")

    def set_color(self, color):
        self.my_color = color

    def get_fen_of_current_state(self):
        board = self.get_board()
        board_fen = self.board_to_fen(board)
        castling_fen = self.castling_availability_to_fen()
        color_fen = self.my_color
        if not self.is_bot():
            player_clock = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'clock-player-turn')]")
            if len(player_clock) == 0:
                raise Exception("You are not in game!")
            if "white" in player_clock[0].get_attribute("class"):
                color_fen = "w"
            else:
                color_fen = "b"
        else:
            color_fen = self.my_color
        try :
            if self.has_anyone_moved():
                return self.get_fen_of_current_state()
        except ValueError:
            return self.get_fen_of_current_state()
        return f"{board_fen} {color_fen} {castling_fen} - 0 1"

    def is_bot(self):
        bot = self.driver.find_elements(By.XPATH, "//wc-chess-board[@id='board-play-computer']")
        if len(bot) > 0:
            return True
        return False

    def is_in_game(self):
        in_game = self.driver.find_elements(By.XPATH, "//wc-chess-board[contains(@class, 'board')]")
        if len(in_game) > 0:
            return True
        return False

    def has_game_ended(self):
        c1 = bool(self.driver.find_elements(By.XPATH, "//span[contains(@class, 'undo')]"))
        c2 = bool(self.driver.find_elements(By.XPATH, "//span[contains(@class, 'redo')]"))
        return c1 or c2

    def get_board(self):
        # pieces in format "piece br square-88"
        board = [[" " for _ in range(8)] for _ in range(8)]
        pieces = self.get_list_of_pieces()
        for piece in pieces:
            piece_info = piece.split(" ")
            piece_info.sort(key=len)

            piece_name = piece_info[0]
            color = piece_name[0]
            figure = piece_name[1]

            piece_postion = piece_info[2].split("-")[1]
            column = int(piece_postion[0]) - 1
            row = int(piece_postion[1]) - 1
            board[7-row][column] = figure if color == 'b' else figure.upper()
        return board

    def board_to_fen(self, board):
        fen_rows = []

        for row in board:
            empty_count = 0
            fen_row = ""
            for cell in row:
                if cell == " ":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += cell
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)
    
        fen_board = "/".join(fen_rows)

        return fen_board

    def has_anyone_moved(self):
        move = None
        pieces = self.get_list_of_pieces()
        if pieces != self.pieces:
            sleep(0.1)
            pieces = self.get_list_of_pieces()
            if len(self.pieces) != 0:
                added = self.pieces - pieces
                removed = pieces - self.pieces
                move = self.what_move_was_made(self.pieces, pieces)
            self.pieces = pieces
            return move
        return move
    
    def what_move_was_made(self, previous_pieces, next_pieces):
        added_pieces = list(next_pieces - previous_pieces)
        removed_pieces = list(previous_pieces - next_pieces)

        if len(added_pieces) + len(removed_pieces) != 2:
            raise ValueError

        added = added_pieces[0].split()
        
        added.sort(key=len)
        figure = added[0]
        for piece in removed_pieces:
            piece_info = piece.split()
            piece_info.sort(key=len)
            if piece_info[0] == figure:
                removed = piece_info
        
        move_to = added[2].split("-")[1]
        move_from = removed[2].split("-")[1]

        return self.board_notation_to_algebraic(move_from, move_to)


    def board_notation_to_algebraic(self, move_from, move_to):
        translation = {
        '1': 'a', '2': 'b', '3': 'c', '4': 'd',
        '5': 'e', '6': 'f', '7': 'g', '8': 'h'
        }
        return f"{translation[move_from[0]]}{move_from[1]}{translation[move_to[0]]}{move_to[1]}"
        
    def is_begining_of_game(self):
        pieces = self.pieces
        for piece in pieces:
            row = int(piece[-1])
            if 2 < row < 7:
                return False
        return True

    def castling_availability_to_fen(self):
        expected_pieces_positions = {
            "bk":("58",),
            "br":("18", "88"),
            "wk":("51",),
            "wr":("11", "81")
        }

        fen_castling = list("KQkq")
        index_at_fen_castling = {
            "81":[0],
            "11":[1],
            "88":[2],
            "18":[3],
            "58":[2,3],
            "51":[0,1]
        }
        
        self.pieces = self.get_list_of_pieces()
        pieces = self.pieces
        current_positions = {piece[16:18] for piece in pieces}

        for piece_type, expected_positions in expected_pieces_positions.items():
            for position in expected_positions:
                if position not in current_positions:
                    indexes = index_at_fen_castling.get(position, [])
                    for index in indexes:
                        fen_castling[index] = ''

        result = "".join(fen_castling)
        return result if result else "-"

    def get_list_of_pieces(self):
        pieces_info = self.driver.find_elements(By.XPATH, "//div[contains(concat(' ', normalize-space(@class), ' '), ' piece ')]")
        pieces = set()
        if len(pieces_info) > 0:         
            for element in pieces_info:
                piece = element.get_attribute("class").removesuffix(" dragging")
                if piece != "element-pool":
                    pieces.add(piece)
        return pieces

    def set_my_color(self, color):
        self.my_color = color

    def Move(self, move, colour, mode):
        ac = ActionChains(self.driver)
        if mode == "live":
            elem = self.driver.find_element_by_id("board-layout-chessboard")
        elif mode == "bot":
            elem = self.driver.find_element_by_id("board-vs-personalities")
        size = elem.size["height"]
        chunk = size/8
        if colour == "white":
            clr = white
        else:
            clr = black
        x1 = (chunk * clr[move[0]]) - (chunk / 2)
        y1 = (chunk * clr[move[1]]) - (chunk / 2)
        x2 = (chunk * clr[move[2]]) - (chunk / 2)
        y2 = (chunk * clr[move[3]]) - (chunk / 2)
        ac.move_to_element_with_offset(elem, x1, y1).click()
        ac.move_to_element_with_offset(elem, x2, y2).click()
        ac.perform()


if __name__ == "__main__":
    bot = Bot(email="", password="")
    bot.log_in()
    while True:
        input()
        print(bot.get_fen_of_current_state())