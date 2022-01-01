import sys
import os
from PyQt5 import QtCore, QtWidgets, QtGui

import chirper


class ChirperApp(QtWidgets.QMainWindow):

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
        self.main_window.start()
        self.setCentralWidget(self.main_window)

        self.make_permanent_status_bar()
        self.show()

    def add_entry_to_menu(self, title, bar, shortcut=None, on_pressed=None):
        act = QtWidgets.QAction(title, bar)
        if shortcut:
            act.setShortcut(shortcut)
        if on_pressed:
            act.triggered.connect(on_pressed)
        bar.addAction(act)

    def make_menu_bar(self):
        self.bar = self.menuBar()

        self.bar_file = self.bar.addMenu("File")
        self.add_entry_to_menu("&New", self.bar_file, "Ctrl+N", lambda: self.menu_act("New"))
        self.add_entry_to_menu("&Open", self.bar_file, "Ctrl+O", lambda: self.menu_act("Open"))
        self.add_entry_to_menu("&Save", self.bar_file, "Ctrl+S", lambda: self.menu_act("Save"))
        self.add_entry_to_menu("&Save As", self.bar_file, "Ctrl+Shift+S", lambda: self.menu_act("Save As"))

        self.bar_file.addSeparator()

        self.export_menu = self.bar_file.addMenu("Export")
        self.add_entry_to_menu("&csv", self.export_menu, on_pressed=lambda: self.menu_act("csv"))
        self.add_entry_to_menu("&json", self.export_menu, on_pressed=lambda: self.menu_act("json"))
        self.add_entry_to_menu("&wav", self.export_menu, on_pressed=lambda: self.menu_act("wav"))
        self.add_entry_to_menu("&png", self.export_menu, on_pressed=lambda: self.menu_act("png"))

        self.bar_file.addSeparator()

        self.add_entry_to_menu("&Exit", self.bar_file, on_pressed=lambda: self.menu_act("Exit"))

        self.bar_edit = self.bar.addMenu("Edit")
        self.add_entry_to_menu("&Undo", self.bar_edit, "Ctrl+Z", lambda: self.menu_act("Undo"))
        self.add_entry_to_menu("&Redo", self.bar_edit, "Ctrl+Y", lambda: self.menu_act("Redo"))

        self.bar_view = self.bar.addMenu("View")
        self.add_entry_to_menu("&Zoom", self.bar_view, on_pressed=lambda: self.menu_act("Zoom"))
        self.add_entry_to_menu("&Fit to content", self.bar_view, on_pressed=lambda: self.menu_act("Fit to content"))

        self.bar_help = self.bar.addMenu("Help")
        self.add_entry_to_menu("&README", self.bar_help, on_pressed=lambda: self.menu_act("README"))
        self.add_entry_to_menu("&Visit webpage", self.bar_help, on_pressed=lambda: self.menu_act("Visit webpage"))

    def menu_act(self, btn, dur=5000):
        self.statusBar().showMessage(f"Pressed {btn}", dur)

    def new_act(self):
        self.statusBar().showMessage("Pressed New", 5000)

    def open_act(self):
        self.statusBar().showMessage("Pressed Open", 5000)

    def save_act(self):
        self.statusBar().showMessage("Pressed Save", 5000)

    def saveas_act(self):
        self.statusBar().showMessage("Pressed Save As", 5000)


    def make_permanent_status_bar(self):
        status_bar_msg = f"Chirper v{chirper.__version__} - For more information, visit the <a href='https://github.com/No-tengo-nombre/chirper'>GitHub repo</a>."
        self.status_lbl = QtWidgets.QLabel(status_bar_msg)
        self.statusBar().addPermanentWidget(self.status_lbl)

    def log_msg(self, msg):
        print(msg)


class ChirperMainWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

    def start(self):
        config_widget = ChirperConfigWidget(self)
        data_widget = ChirperDataWidget(self)
        config_widget.start()
        data_widget.start()

        self.layout.addWidget(config_widget, 2)
        self.layout.addWidget(data_widget, 4)

    def log_msg(self, msg):
        self.parent().log_msg(msg)


class ChirperConfigWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

    def start(self):
        pass
        # btn1 = QtWidgets.QPushButton("Test button 1", self)
        # btn1.setToolTip("This is a test button 1")
        # btn1.clicked.connect(lambda: self.on_click("btn1 was pressed"))

        # btn2 = QtWidgets.QPushButton("Test button 2", self)
        # btn2.setToolTip("This is a test button 2")
        # btn2.clicked.connect(lambda: self.on_click("btn2 was pressed"))

        # self.layout.addWidget(btn1)
        # self.layout.addWidget(btn2)

    def make_options_entry(self, msg, options):
        entry_layout = QtWidgets.QHBoxLayout()
        text_box = QtWidgets.QLabel(msg, entry_layout)
        # options_box = QtWidgets.QMnu

    @QtCore.pyqtSlot()
    def on_click(self, msg):
        self.parent().log_msg(msg)


class ChirperDataWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

    def start(self):
        btn1 = QtWidgets.QPushButton("Test button 1", self)
        btn1.setToolTip("This is a test button 1")
        btn1.clicked.connect(lambda: self.on_click("btn1 was pressed"))

        btn2 = QtWidgets.QPushButton("Test button 2", self)
        btn2.setToolTip("This is a test button 2")
        btn2.clicked.connect(lambda: self.on_click("btn2 was pressed"))

        btn3 = QtWidgets.QPushButton("Test button 3", self)
        btn3.setToolTip("This is a test button 3")
        btn3.clicked.connect(lambda: self.on_click("btn3 was pressed"))

        self.layout.addWidget(btn1)
        self.layout.addWidget(btn2)
        self.layout.addWidget(btn3)

    @QtCore.pyqtSlot()
    def on_click(self, msg):
        self.parent().log_msg(msg)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = ChirperApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
