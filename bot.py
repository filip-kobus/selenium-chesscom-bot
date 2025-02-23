from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller


class Xpaths:
    email = "//input[@type='email']"
    password = "//input[@type='password']"
    login_button = "//button[@type='submit']"
    board = "//wc-chess-board[contains(@class, 'board')]"
    promotion_piece = "//div[contains(@class, 'promotion-piece')]"

class Scripts:
    get_fen = """
            return document.querySelector("wc-chess-board").game.getFEN();
        """
    get_last_move = """
            return document.querySelector("wc-chess-board").game.getLastMove();
        """
    is_game_over = """
            return document.querySelector("wc-chess-board").game.isGameOver();
        """
    get_mode = """
            return document.querySelector("wc-chess-board").game.getMode().name;
        """
    get_color = """
            return document.querySelector("wc-chess-board").game.getPlayingAs();
        """

class Bot:
    URL = "https://www.chess.com/login"

    def __init__(self):
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()
        self.xpaths = Xpaths
        self.scripts = Scripts
        self.current_move = None
        self.color = None

    def open_page(self):
        self.driver.get(self.URL)
        self.driver.maximize_window()

    def log_in(self, email, password):
        try:
            WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, self.xpaths.email))).send_keys(email)
            WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, self.xpaths.password))).send_keys(password)
            WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, self.xpaths.login_button))).click()
        except TimeoutException:
            print("Unable to log in. Do it manually.")

    def is_on_board(self):
        on_board = self.driver.find_elements(By.XPATH, self.xpaths.board)
        if len(on_board) > 0:
            return True
        return False

    def get_board_fen(self):
        fen = self.driver.execute_script(self.scripts.get_fen)
        return fen

    def has_anyone_moved(self):
        current_move = self.driver.execute_script(self.scripts.get_last_move)
        if current_move != self.current_move:
            self.current_move = current_move
            return True
        return False

    def is_game_over(self):
       return self.driver.execute_script(self.scripts.is_game_over)

    def is_in_game(self):
        mode = self.driver.execute_script(self.scripts.get_mode)
        if mode == "playing":
            return True
        return False
    
    def get_player_color(self):
        color = self.driver.execute_script(self.scripts.get_color)
        if color == 1:
            self.color = 'w'
        else:
            self.color = 'b'
        return self.color

    def make_move(self, move):
        board_element = self.driver.find_element(By.XPATH, self.xpaths.board)
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
