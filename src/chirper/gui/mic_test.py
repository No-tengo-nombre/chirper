import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets
import sys

from ..api import GuiInterface


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.gui = GuiInterface()
        self.blocksize = 400
        # self.r1 = 0
        # self.r1 = self.blocksize // 2
        # self.r2 = self.blocksize // 2
        # self.r2 = self.blocksize
        self.values = np.zeros((1, 1))

        self.fig = pg.image(self.values)
        self.fig.setColorMap(pg.colormap.get("plasma"))

        self.send_start_request()

        self.timer = pg.Qt.QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def image(self, data):
        return self.graphWidget.image(data)

    def update_plot_data(self):
        # self.values = self.values[:, 1:]

        # max_time = 2

        new_values = self.send_fetch_request()
        # if new_values.ax0_span() > max_time:
        #     end_time = new_values.ax0[-1]
        #     new_values = new_values.get_ax0(end_time - max_time)

        self.fig.setImage(new_values.values)
        # self.values = np.vstack((self.values.T, new_col)).T

        # self.fig.setImage(self.values.T)

    def send_start_request(self):
        self.gui.make_request({
            "request_type": "start",
            "source": "microphone",
        })

    def send_fetch_request(self):
        return self.gui.make_request({
            "request_type": "spectrogram",
            "source": "microphone",
            "blocksize": self.blocksize,
            "max_time": 2,
        })

    def send_stop_request(self):
        self.gui.make_request({
            "request_type": "stop",
            "source": "microphone",
        })


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
