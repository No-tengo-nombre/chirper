import sys
import os
import logging
import pyqtgraph as pg
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui

import chirper
from ..api import GuiInterface

########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||| Main GUI definitions |||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


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
        # self.main_window.start()
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
        logging.info(msg)


class ChirperMainWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.start()

    def start(self):
        self.config_widget = ChirperConfigWidget(self)
        self.data_widget = ChirperDataWidget(self)
        # self.config_widget.start()
        # self.data_widget.start()

        self.layout.addWidget(self.config_widget)
        # self.layout.addWidget(data_widget, 2)
        self.layout.addWidget(self.data_widget.fig, 2)

    def log_msg(self, msg):
        self.parent().log_msg(msg)


class ChirperConfigWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
        self.start()

    def start(self):
        self.source_options = [
            "microphone",
            "Test1",
            "Test2",
            "Test3",
            "Test4",
        ]

        self.source_btns = [
            # ("On", lambda: logging.info("Source turned ON")),
            # ("Off", lambda: logging.info("Source turned OFF")),
            ("On", self.source_on_event),
            ("Off", self.source_off_event),
        ]

        self.types_options = [
            "spectrogram",
            "Type test 1",
            "Type test 2",
            "Type test 3",
            "Type test 4",
        ]

        self.console_options = [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ]

        self.title_entry = self.make_options_entry(
            "<h2>Configuration</h2><hr>"
        )
        self.source_entry = self.make_options_entry(
            "Source",
            self.source_options,
            self.source_btns,
            self.source_options_event,
            0,
            self.source_options_default,
        )
        self.types_entry = self.make_options_entry(
            "Visualization",
            self.types_options,
            None,
            self.type_options_event,
            0,
            self.type_options_default,
        )
        self.blocksize_entry = self.make_number_config(
            "Blocksize",
            500,
            lambda: self.blocksize_event(self.blocksize_entry),
            self.blocksize_default,
        )
        self.samprate_entry = self.make_number_config(
            "Sampling rate",
            44100,
            lambda: self.samplerate_event(self.samprate_entry),
            self.samplerate_default,
        )
        self.maxtime_entry = self.make_number_config(
            "Maximum time",
            2,
            lambda: self.maxtime_event(self.maxtime_entry),
            self.maxtime_default,
        )
        self.channels_entry = self.make_number_config(
            "Channels",
            1,
            lambda: self.channels_event(self.channels_entry),
            self.channels_default,
        )
        self.console_config_entry = self.make_options_entry(
            "Console level",
            self.console_options,
            options_event=lambda: self.console_options_event(
                self.console_config_entry),
            default_index=2,
        )

        self.output_console_box = self.make_console_box()
        self.input_console_box = self.make_input_console_box()

        self.output_console_box.setFormatter(
            logging.Formatter("%(levelname)s - %(message)s"))
        self.output_console_box.setReadOnly(True)
        logging.getLogger().addHandler(self.output_console_box)

        self.input_console_box.setPlaceholderText("Chirper console")

        console_clear_btn = QtWidgets.QPushButton("Clear console")
        console_clear_btn.clicked.connect(
            lambda: self.output_console_box.setText(""))
        self.console_config_entry.layout().addWidget(console_clear_btn)

        self.log(f"""
        request type {self.request_type}
        source {self.source}
        blocksize {self.blocksize}
        samplerate {self.samplerate}
        max time {self.max_time}
        channels {self.channels}
        """)

    def source_options_event(self, entry):
        option_index = entry.options_box.currentIndex()
        self.source = self.source_options[option_index]

    def source_options_default(self, index):
        self.source = self.source_options[index]

    def type_options_event(self, entry):
        option_index = entry.options_box.currentIndex()
        self.request_type = self.types_options[option_index]

    def type_options_default(self, index):
        self.request_type = self.types_options[index]

    def blocksize_event(self, entry):
        value = entry.input_box.text()
        try:
            self.blocksize = int(value)
            logging.info(f"Set blocksize to {self.blocksize}")
        except ValueError:
            logging.warning(f"Can't understand {value} as int.")

    def samplerate_event(self, entry):
        value = entry.input_box.text()
        try:
            self.samplerate = int(value)
            logging.info(f"Set samplerate to {self.samplerate}")
        except ValueError:
            logging.warning(f"Can't understand {value} as int.")

    def maxtime_event(self, entry):
        value = entry.input_box.text()
        try:
            self.max_time = float(value)
            logging.info(f"Set max time to {self.max_time}")
        except ValueError:
            logging.warning(f"Can't understand {value} as float.")

    def channels_event(self, entry):
        value = entry.input_box.text()
        try:
            self.channels = int(value)
            logging.info(f"Set channels to {self.channels}")
        except ValueError:
            logging.warning(f"Can't understand {value} as int.")

    def blocksize_default(self, value):
        try:
            self.blocksize = int(value)
            logging.info(f"Set blocksize to {self.blocksize}")
        except ValueError:
            logging.warning(f"Can't understand {value} as int.")

    def samplerate_default(self, value):
        try:
            self.samplerate = int(value)
            logging.info(f"Set samplerate to {self.samplerate}")
        except ValueError:
            logging.warning(f"Can't understand {value} as int.")

    def maxtime_default(self, value):
        try:
            self.max_time = float(value)
            logging.info(f"Set max time to {self.max_time}")
        except ValueError:
            logging.warning(f"Can't understand {value} as float.")

    def channels_default(self, value):
        try:
            self.channels = int(value)
            logging.info(f"Set channels to {self.channels}")
        except ValueError:
            logging.warning(f"Can't understand {value} as int.")

    def source_on_event(self):
        data_widget = self.parent().data_widget
        data_widget.set_source(self.source)
        data_widget.send_start_request()

        data_widget.fetch_request["request_type"] = self.request_type
        data_widget.fetch_request["blocksize"] = self.blocksize
        data_widget.fetch_request["samplerate"] = self.samplerate
        data_widget.fetch_request["max-time"] = self.max_time
        data_widget.fetch_request["channels"] = self.channels
        data_widget.start_fetch()

    def source_off_event(self):
        data_widget = self.parent().data_widget

        data_widget.stop_fetch()
        data_widget.send_stop_request()
        data_widget.clear_image()

    def console_options_event(self, entry):
        options = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]
        option_index = entry.options_box.currentIndex()
        logging.getLogger().setLevel(options[option_index])

    def make_options_entry(self, msg=None, options=None, btns=None, options_event=None, default_index=None, default_setter=None):
        entry = QtWidgets.QWidget()
        entry_layout = QtWidgets.QHBoxLayout()
        entry_layout.setAlignment(QtCore.Qt.AlignLeft)
        entry.setLayout(entry_layout)

        if msg is not None:
            entry.text_box = QtWidgets.QLabel(msg)
            entry_layout.addWidget(entry.text_box)

        if options is not None:
            entry.options_box = QtWidgets.QComboBox()
            entry.options_box.addItems(options)
            if default_index is not None:
                entry.options_box.setCurrentIndex(default_index)
                if default_setter is not None:
                    default_setter(default_index)
            if options_event is not None:
                entry.options_box.activated.connect(options_event)
            entry_layout.addWidget(entry.options_box)

        if btns is not None:
            entry.btns = []
            for btn, *action in btns:
                option = QtWidgets.QRadioButton(btn)
                if action is not None:
                    option.clicked.connect(*action)
                entry_layout.addWidget(option)
                entry.btns.append(option)

        self.layout.addWidget(entry)
        return entry

    def make_number_config(self, msg, default=None, enter_event=None, default_setter=None):
        entry = QtWidgets.QWidget()
        entry_layout = QtWidgets.QHBoxLayout()
        entry_layout.setAlignment(QtCore.Qt.AlignLeft)
        entry.setLayout(entry_layout)

        if msg is not None:
            entry.text_box = QtWidgets.QLabel(msg)
            entry_layout.addWidget(entry.text_box)

        entry.input_box = QtWidgets.QLineEdit()
        if default is not None:
            entry.input_box.setText(str(default))
            if default_setter is not None:
                default_setter(default)
        if enter_event is not None:
            entry.input_box.returnPressed.connect(enter_event)
        entry_layout.addWidget(entry.input_box)

        self.layout.addWidget(entry)
        return entry

    def make_console_box(self):
        console = ConsoleBox()
        console.setFont(QtGui.QFont("Courier New"))
        self.layout.addWidget(console)
        return console

    def make_input_console_box(self):
        console = InputConsoleBox()
        console.setFont(QtGui.QFont("Courier New"))
        self.layout.addWidget(console)
        return console

    def log(self, msg):
        self.output_console_box.append(msg)


class ChirperDataWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super(QtWidgets.QWidget, self).__init__(*args, **kwargs)
        self.gui = GuiInterface()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.start(*args, **kwargs)

    # def start(self, blocksize=500, cmap=None, *args, **kwargs):
    def start(self, *args, cmap=None, **kwargs):
        # self.blocksize = blocksize
        self.start_request = {
            "request_type": "start",
        }
        self.fetch_request = {}
        self.stop_request = {
            "request_type": "stop",
        }
        self.empty_values = np.zeros((1, 1))

        self.fig = pg.image(self.empty_values)

        if cmap is not None:
            self.fig.setColorMap(pg.colormap.get(cmap))
        else:
            self.fig.setColorMap(pg.colormap.get("plasma"))

        self.layout.addWidget(self.fig)

    def clear_image(self):
        self.fig.clear()

    def set_source(self, source):
        self.source = source
        self.start_request["source"] = source
        self.stop_request["source"] = source
        self.fetch_request["source"] = source

    def start_fetch(self, interval=20):
        self.timer = pg.Qt.QtCore.QTimer()
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def stop_fetch(self):
        self.timer.stop()

    def update_plot_data(self):
        new_values = self.send_fetch_request()
        self.fig.setImage(new_values.values)

    def send_request(self, request: dict):
        logging.info(f"Send request {request}")
        return self.gui.make_request(request)

    def send_start_request(self):
        logging.info(f"Send start request {self.start_request}")
        return self.gui.make_request(self.start_request)

    def send_fetch_request(self):
        logging.info(f"Send fetch request {self.fetch_request}")
        return self.gui.make_request(self.fetch_request)

    def send_stop_request(self):
        logging.info(f"Send stop request {self.stop_request}")
        return self.gui.make_request(self.stop_request)


########################################################################################################################
# |||||||||||||||||||||||||||||||||||||||||||||||| Console Box ||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


class ConsoleBox(QtWidgets.QTextEdit, logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        self.append(msg)

    def append(self, text: str) -> None:
        return super().append(f">>> {text}")


class InputConsoleBox(QtWidgets.QLineEdit):
    pass


########################################################################################################################
# ||||||||||||||||||||||||||||||||||||||||||||||| Main function |||||||||||||||||||||||||||||||||||||||||||||||||||||| #
########################################################################################################################


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = ChirperApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
