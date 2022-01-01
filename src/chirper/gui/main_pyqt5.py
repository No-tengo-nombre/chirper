import sys
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QFrame, QGridLayout, QLabel, QWidget, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon, QTextBlock

import chirper


class ChirperApp(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.title = "Test"
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480

        self.init_ui()

    def set_stylesheet(self, filename):
        with open(filename, "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

    def init_ui(self):
        self.set_stylesheet(os.path.join(
            chirper.BASE_DIRNAME, "gui/css/styles.css"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.make_menu_bar()

        self.main_window = ChirperMainWidget(self)
        self.main_window.layout = QGridLayout()
        self.main_window.setLayout(self.main_window.layout)
        self.main_window.start()
        self.setCentralWidget(self.main_window)

        self.make_permanent_status_bar()
        self.show()

    def make_menu_bar(self):
        self.bar = self.menuBar()

        self.bar_file = self.bar.addMenu("File")
        self.bar_file.addAction("New")
        self.bar_file.addAction("Open")
        self.bar_file.addAction("Save")
        self.bar_file.addAction("Save As")
        self.bar_file.addSeparator()
        self.export_menu = self.bar_file.addMenu("Export")
        self.export_menu.addAction("CSV")
        self.export_menu.addAction("JSON")
        self.export_menu.addAction("WAV")
        self.export_menu.addAction("PNG")
        self.bar_file.addSeparator()
        self.bar_file.addAction("Exit")

        self.bar_view = self.bar.addMenu("View")
        self.bar_view.addAction("Zoom")
        self.bar_view.addAction("Fit to content")

        self.bar_help = self.bar.addMenu("Help")
        self.bar_help.addAction("README")
        self.bar_help.addAction("Visit webpage")

    def make_permanent_status_bar(self):
        status_bar_msg = f"Chirper v{chirper.__version__} - For more information, visit the <a href='https://github.com/No-tengo-nombre/chirper'>GitHub repo</a>."
        self.status_lbl = QLabel(status_bar_msg)
        self.statusBar().addPermanentWidget(self.status_lbl)


class ChirperMainWidget(QWidget):
    def start(self):
        btn = QPushButton("Test button", self)
        btn.setToolTip("This is a test button")
        btn.clicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("The button was pressed")


def main():
    app = QApplication(sys.argv)
    ex = ChirperApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
