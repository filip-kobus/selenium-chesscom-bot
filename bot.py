from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from engine import engine
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

black = {"a" : 8,"1" : 1,
        "b" : 7, "2" : 2,
        "c" : 6, "3" : 3,
        "d" : 5, "4" : 4,
        "e" : 4, "5" : 5,
        "f" : 3, "6" : 6,
        "g" : 2, "7" : 7,
        "h" : 1, "8" : 8,}

white = {"a" : 1, "8" : 1,
        "b" : 2, "7" : 2,
        "c" : 3, "6" : 3,
        "d" : 4, "5" : 4,
        "e" : 5, "4" : 5,
        "f" : 6, "3" : 6,
        "g" : 7, "2" : 7,
        "h" : 8, "1" : 8,}

class Bot:

    Path = r"config\chromedriver.exe"

    def __init__(self, url = "https://www.chess.com/pl/login", passwd = "", usr = ""):
        self.passwd = passwd
        self.usr = usr
        self.url = url
        self.driver = webdriver.Chrome(self.Path)
        self.card = self.driver.get(self.url)
        self.driver.maximize_window()

    def openPage(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.usr)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(self.passwd)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login"))).click()
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
               (By.CSS_SELECTOR, "button[class^='accept-button']"))).click()
        except:
            pass

    def BotOrLive(self):
        c1 = self.driver.find_elements_by_id("board-layout-chessboard")
        c2 = self.driver.find_elements_by_id("board-vs-personalities")
        c3 = self.driver.find_elements_by_css_selector("span[class='icon-font-chess circle-gearwheel daily-game-footer-icon']")
        c4 = self.driver.find_elements_by_css_selector("a[class='eco-opening-text']")
        if len(c1) > len(c2) and len(c3) < 1:
            return "live"
        elif len(c3) == 1:
            return  "daily"
        elif len(c2) == 1:
            return "bot"
        elif len(c4) == 0:
            return None
        else:
            return None

    def BlackOrWhite(self):
        cords = self.driver.find_elements_by_css_selector("text[class^='coordinate-']")
        if len(cords) == 0:
            return None
        if cords[8].text == "a":
            return "white"
        else: return "black"

    def checkIfGameEnd(self):
        c1 = self.driver.find_elements_by_css_selector("span[class$='undo']")
        c2 = self.driver.find_elements_by_css_selector("span[class$='arrow-right']")
        if len(c1) < 1 and len(c2) < 1:
            return True  #game didn't end
        else:
            return False #game ended

    def whiteOrBlackMove(self, colour):
        w = self.driver.find_elements_by_css_selector("div[class='black node selected']")
        b = self.driver.find_elements_by_css_selector("div[class='white node selected']")
        wn = self.driver.find_elements_by_css_selector("div[class='white node']")

        if (colour == "white" and len(w) > 0) or (colour == "white" and len(wn) == 0 and len(b) == 0):
            return True
        elif colour == "white" and len(w) == 0:
            return False
        elif colour != "white" and len(b) > 0:
            return True
        elif colour != "white" and len(b) == 0:
            return False

    def getPosition(self):
        black = self.driver.find_elements_by_css_selector("div[class='black node selected']")
        white = self.driver.find_elements_by_css_selector("div[class='white node selected']")
        if len(black) > len(white):
            var = black
        elif len(black) < len(white):
            var = white
        else: return None
        elem = var[0].find_elements_by_css_selector("span[class^='icon-font']")
        if len(elem) > 0:
            if "=" in var[0].text:
                string = ''
                figurine = str(elem[0].get_attribute("data-figurine"))
                for i2 in range(len(var[0].text)):
                    string += var[0].text[i2]
                    if var[0].text[i2] == "=":
                        string += figurine
                return string
            else:
                if "None" in str(elem[0].get_attribute("data-figurine")):
                    return var[0].text
                else:
                    return str(elem[0].get_attribute("data-figurine")) + var[0].text
        else:
            return var[0].text

    def movesBeforeLaunch(self):
        list = []
        moves = self.driver.find_elements_by_css_selector("div[class$='node']")
        for i in range(len(moves)):
            elem = moves[i].find_elements_by_css_selector("span[class^='icon-font']")
            if len(elem) > 0:
                if "=" in moves[i].text:
                    string = ''
                    figurine = str(elem[0].get_attribute("data-figurine"))
                    for i2 in range(len(moves[i].text)):
                        string += moves[i].text[i2]
                        if moves[i].text[i2] == "=":
                            string += figurine
                    list.append(string)
                else:
                    list.append(str(elem[0].get_attribute("data-figurine")) + moves[i].text)
            else:
                list.append(moves[i].text)
        return list

    def pickFigurine(self, mode):
        if mode == "bot":
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[4]/div[4]/div[1]/a[3]"))).click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body/div[2]/div[9]/div/div[2]/div/div[2]/div/div[5]/div/select/option[1]"))).click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[class^='ui_icon-font-component icon-font-chess x modal-close']"))).click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[4]/div[4]/div[1]/a[3]"))).click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body/div[2]/div[9]/div/div[2]/div/div[2]/div/div[5]/div/select/option[2]"))).click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[class^='ui_icon-font-component icon-font-chess x modal-close']"))).click()

        else:
            for i in range(1,3):
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button[class^='icon-font-chess circle-gearwheel']"))).click()

                if i == 1:
                    value = "text"
                else: value = "figurine"

                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "option[value ='"+value+"']"))).click()

                elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "button[class^='ui_v5-button-component ui_v5-button-primary settings-modal-container-button']")))

                if elem.get_attribute("disabled") == "true":
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR,
                         "button[class^='ui_v5-button-component ui_v5-button-basic-light settings-modal-container-button']"))).click()
                else:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR,
                         "button[class^='ui_v5-button-component ui_v5-button-primary settings-modal-container-button']"))).click()

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
    pass
