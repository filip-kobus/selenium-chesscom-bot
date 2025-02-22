from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller


class XPATHS:
    email = "//input[@type='email']"
    password = "//input[@type='password']"
    login_button = "//button[@type='submit']"
    in_game_indicator = "//wc-chess-board[contains(@class, 'board')]"


class Bot:
    chromedriver_autoinstaller.install()
    PATH = "chromedriver.exe"
    URL = "https://www.chess.com/pl/login"

    def __init__(self, url=URL, password="", email=""):
        self.password = password
        self.email = email
        self.url = url
        self.driver = webdriver.Chrome(self.PATH)
        self.card = self.driver.get(self.url)
        self.driver.maximize_window()
        self.current_move = None
        self.color = None

    def log_in(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(self.email)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(self.password)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))).click()
        except Exception:
            print("Unable to log in. Do it manually.")

    def is_on_board(self):
        in_game = self.driver.find_elements(By.XPATH, "//wc-chess-board[contains(@class, 'board')]")
        if len(in_game) > 0:
            return True
        return False

    def get_board_fen(self):
        fen = self.driver.execute_script("""
            return document.querySelector("wc-chess-board").game.getFEN();
        """)
        return fen

    def has_anyone_moved(self):
        current_move = self.driver.execute_script("""
            return document.querySelector("wc-chess-board").game.getLastMove();
        """)
        if current_move != self.current_move:
            self.current_move = current_move
            return True
        return False

    def is_game_over(self):
       return self.driver.execute_script("""
            return document.querySelector("wc-chess-board").game.isGameOver();
        """)

    def is_in_game(self):
        mode = self.driver.execute_script("""
            return document.querySelector("wc-chess-board").game.getMode().name;
        """)
        if mode == "playing":
            return True
        return False
    
    def get_player_color(self):
        color = self.driver.execute_script("""
            return document.querySelector("wc-chess-board").game.getPlayingAs();
        """)
        if color == 1:
            self.color = 'w'
        else:
            self.color = 'b'
        return self.color

    def make_move(self, move):
        board_element = self.driver.find_element(By.XPATH, "//wc-chess-board")
        coordinates = self.move_to_board_coordinates(move, board_element)
        if coordinates is not None:
            from_x, from_y, to_x, to_y = coordinates
            ac = ActionChains(self.driver)

            ac.move_to_element_with_offset(board_element, from_x, from_y).click()
            ac.move_to_element_with_offset(board_element, to_x, to_y).click()
            ac.perform()
        else:
            return
        if len(move) == 5:
            promotion_piece = self.color + move[4]
            promotion_piece_xpath = f"//div[contains(@class, 'promotion-piece') and contains(@class, '{promotion_piece}')]"
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, promotion_piece_xpath))).click()
            except Exception:
                pass

    def move_to_board_coordinates(self, move, board_element):
        size = board_element.size
        width = size['width']
        cell_size = width / 8
        cell_middle = int(cell_size / 2)

        translation = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4,
            'e': 5, 'f': 6, 'g': 7, 'h': 8
        }

        move = list(move)

        if self.color == 'b':
            from_x = (8 - translation[move[0]]) * cell_size + cell_middle
            from_y = (int(move[1]) - 1) * cell_size + cell_middle
            to_x = (8 - translation[move[2]]) * cell_size + cell_middle
            to_y = (int(move[3]) - 1) * cell_size + cell_middle

        else:
            from_x = (translation[move[0]] - 1) * cell_size + cell_middle
            from_y = (8 - int(move[1])) * cell_size + cell_middle
            to_x = (translation[move[2]] - 1) * cell_size + cell_middle
            to_y = (8 - int(move[3])) * cell_size + cell_middle

        return from_x, from_y, to_x, to_y

if __name__ == "__main__":
    pass
