# ♟ Selenium Chess.com Bot

A **fully automated Chess.com bot** built using **Python, Selenium, and Stockfish**.\
It can log in, play moves automatically, and analyze games using **Stockfish**.

---

## 🎯 Features

✅ **Automated Chess.com Gameplay** – Plays chess moves using Stockfish.\
✅ **Selenium Web Automation** – Logs in and interacts with the Chess.com board.\
✅ **Stockfish Integration** – Uses Stockfish engine for best moves.\
✅ **Auto-Move Timer** – Configurable countdown for automatic moves.\
✅ **GUI with PyQt5** – Simple user interface for easy control.

---

## 📚 Project Structure

```
selenium-chesscom-bot/
│── config/                     # Configuration files
│   ├── settings.json            # Bot settings
│   ├── user.json                # User credentials
│   ├── stockfish.exe            # Stockfish engine
│   ├── icon.ico                 # App icon
│
│── src/                         # Main source code
│   ├── main.py                  # Entry point
│   ├── bot.py                   # Core bot logic
│   ├── engine.py                # Stockfish engine integration
│   ├── bot_worker.py            # Handles bot execution
│   ├── login_worker.py          # Manages login process
│   ├── timer_worker.py          # Handles countdown timer
│   ├── selenium_helpers.py      # Utility functions for Selenium
│
│── gui/                         # UI-related files
│   ├── app_window.py            # GUI logic
│   ├── Ui_MainWindow.py         # Auto-generated PyQt5 UI code
│   ├── Ui_MainWindow.ui         # UI design file
│
│── tests/                       # Unit and functional tests
│── venv/                        # Virtual environment
│── requirements.txt             # Python dependencies
│── README.md                    # Documentation
│── .gitignore                    # Git ignore settings
│── start.sh                      # Shell script to start the bot
```

---

## 🛠 Installation

### **1️⃣ Create virtual environment**

Make sure you have **Python 3.8+** installed.\
Then, make venv:

```sh
python -m venv .venv
```

### **2️⃣ Activate virtual environment**

```sh
source .venv/Scripts/activate
```


### **3️⃣ Install requirements & Google Chrome**

- Download **Google Chrome**: [https://www.google.com/chrome/](https://www.google.com/chrome/)
- Install requirements
```sh
pip install -r requirements
```

### **4️⃣ Run the Bot**

```sh
python main.py
```

---

## 🖥️ **Usage**

 **Video Presentation**:
[![Watch the demo](https://img.youtube.com/vi/lH6JCJVjvCI/maxresdefault.jpg)](https://www.youtube.com/watch?v=lH6JCJVjvCI)

---


## 🤝 Credits

Developed by [Filip Kobus](https://github.com/filip-kobus)\
Built with **Python, Selenium, PyQt5, and Stockfish**.

---
