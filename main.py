import sys  # Required for command-line arguments and exiting the application
from PyQt5.QtWidgets import QApplication  # The main application class
from app_window import MainWindow  # Assuming you have a MainWindow class in `main_window.py`

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())