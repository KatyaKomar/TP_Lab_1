import sys

from PyQt5.QtWidgets import QApplication

from ui.interface import MainWindow


def start():
    """Paint application entry point"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    start()