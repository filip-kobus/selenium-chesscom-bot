# ♟ Selenium Chess.com Bot

A **fully automated Chess.com bot** built using **Python, Selenium, and Stockfish**.\
It can log in, play moves automatically, and analyze games using **Stockfish**.

---

## 🎯 Features

✅ **Selenium Web Automation** – Logs in and interacts with the Chess.com board.\
✅ **Stockfish Integration** – Uses Stockfish engine for best moves.\
✅ **GUI with PyQt5** – Simple user interface.\

---

## 📚 Project Structure

```
selenium-chesscom-bot/
│── config/                     # Configuration files
│   ├── icon.ico                 # Application icon
│   ├── settings.json            # Bot settings
│   ├── user.json                # User credentials
│   ├── stockfish.exe            # Stockfish engine
│
│── gui/                         # GUI-related files
│   ├── app_window.py            # GUI logic
│   ├── Ui_MainWindow.py         # Auto-generated PyQt5 UI code
│   ├── Ui_MainWindow.ui         # UI design file
│
│── src/                         # Main source code
│   ├── bot_worker.py            # Handles bot execution
│   ├── bot.py                   # Core bot logic
│   ├── engine.py                # Stockfish engine integration
│   ├── login_worker.py          # Manages login process
│   ├── timer_worker.py          # Handles countdown timer
│
│── venv/                        # Virtual environment
│── README.md                    # Documentation
│── requirements.txt             # Python dependencies
├── main.py                      # Entry point
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
