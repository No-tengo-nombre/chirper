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
        self.add_entry_to_menu("&New", self.bar_file,
                               "Ctrl+N", lambda: self.menu_act("New"))
        self.add_entry_to_menu("&Open", self.bar_file,
                               "Ctrl+O", lambda: self.menu_act("Open"))
        self.add_entry_to_menu("&Save", self.bar_file,
                               "Ctrl+S", lambda: self.menu_act("Save"))
        self.add_entry_to_menu("&Save As", self.bar_file,
                               "Ctrl+Shift+S", lambda: self.menu_act("Save As"))

        self.bar_file.addSeparator()

        self.export_menu = self.bar_file.addMenu("Export")
        self.add_entry_to_menu("&csv", self.export_menu,
                               on_pressed=lambda: self.menu_act("csv"))
        self.add_entry_to_menu("&json", self.export_menu,
                               on_pressed=lambda: self.menu_act("json"))
        self.add_entry_to_menu("&wav", self.export_menu,
                               on_pressed=lambda: self.menu_act("wav"))
        self.add_entry_to_menu("&png", self.export_menu,
                               on_pressed=lambda: self.menu_act("png"))

        self.bar_file.addSeparator()

        self.add_entry_to_menu("&Exit", self.bar_file,
                               "Ctrl+W", self.close)

        self.bar_edit = self.bar.addMenu("Edit")
        self.add_entry_to_menu("&Undo", self.bar_edit,
                               "Ctrl+Z", lambda: self.menu_act("Undo"))
        self.add_entry_to_menu("&Redo", self.bar_edit,
                               "Ctrl+Y", lambda: self.menu_act("Redo"))

        self.bar_view = self.bar.addMenu("View")
        self.add_entry_to_menu("&Zoom", self.bar_view,
                               on_pressed=lambda: self.menu_act("Zoom"))
        self.add_entry_to_menu("&Fit to content", self.bar_view,
                               on_pressed=lambda: self.menu_act("Fit to content"))

        self.bar_help = self.bar.addMenu("Help")
        self.add_entry_to_menu("&README", self.bar_help,
                               on_pressed=lambda: self.menu_act("README"))
        self.add_entry_to_menu("&Visit webpage", self.bar_help,
                               on_pressed=lambda: self.menu_act("Visit webpage"))

    def menu_act(self, btn, dur=5000):
        self.statusBar().showMessage(f"Pressed {btn}", dur)

    def make_permanent_status_bar(self):
        status_bar_msg = f"Chirper v{chirper.__version__} - For more information, visit the <a href='https://github.com/No-tengo-nombre/chirper'>GitHub repo</a>."
        self.status_lbl = QtWidgets.QLabel(status_bar_msg)
        self.statusBar().addPermanentWidget(self.status_lbl)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        reply = QtWidgets.QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to exit the program?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            a0.accept()
        else:
            a0.ignore()

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

        self.layout.addWidget(config_widget)
        self.layout.addWidget(data_widget, 2)

    def log_msg(self, msg):
        self.parent().log_msg(msg)


class ChirperConfigWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)

    def start(self):
        source_options = [
            "Microphone",
            "Test1",
            "Test2",
            "Test3",
            "Test4",
        ]

        source_btns = [
            ("On", lambda: self.log("Source turned ON")),
            ("Off", lambda: self.log("Source turned OFF")),
        ]

        types_options = [
            "Spectrogram",
            "Type test 1",
            "Type test 2",
            "Type test 3",
            "Type test 4",
        ]

        self.title_entry = self.make_options_entry(
            "<h2>Configuration</h2><hr>")
        self.source_entry = self.make_options_entry(
            "Source", source_options, source_btns)
        self.types_entry = self.make_options_entry(
            "Visualization", types_options)
        self.console_box = self.make_console_box()

        self.layout.addWidget(self.title_entry)
        self.layout.addWidget(self.source_entry)
        self.layout.addWidget(self.types_entry)
        self.layout.addWidget(self.console_box)

    def make_options_entry(self, msg=None, options=None, btns=None):
        entry = QtWidgets.QWidget()
        entry_layout = QtWidgets.QHBoxLayout()
        entry_layout.setAlignment(QtCore.Qt.AlignLeft)
        entry.setLayout(entry_layout)

        if msg:
            text_box = QtWidgets.QLabel(msg)
            entry_layout.addWidget(text_box)

        if options:
            options_box = QtWidgets.QComboBox()
            options_box.addItems(options)
            entry_layout.addWidget(options_box)

        if btns:
            for btn, *action in btns:
                option = QtWidgets.QRadioButton(btn)
                if action:
                    option.toggled.connect(*action)
                entry_layout.addWidget(option)

        return entry

    def make_console_box(self):
        console = QtWidgets.QTextEdit()
        console.setFont(QtGui.QFont("Courier New"))
        console.setPlaceholderText("Chirper console")
        return console

    def log(self, msg):
        self.console_box.append(msg)


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
