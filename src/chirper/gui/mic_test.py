import numpy as np
from numpy.core.shape_base import block
import sounddevice as sd
import pyqtgraph as pg
from PyQt5 import QtWidgets
import time
import sys

from .interface import GuiInterface
from chirper.transforms import fourier


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.gui = GuiInterface()
        self.blocksize = 750
        # self.r1 = 0
        self.r1 = self.blocksize // 2
        # self.r2 = self.blocksize // 2
        self.r2 = self.blocksize
        self.values = np.zeros((self.r2 - self.r1, self.r2 - self.r1))


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
        self.values = self.values[:, 1:]

        new_col = self.send_fetch_request()
        self.values = np.vstack((self.values.T, new_col)).T

        self.fig.setImage(self.values.T)

    def send_start_request(self):
        self.gui.make_request({
            "request_type": "start",
            "source": "microphone",
        })

    def send_fetch_request(self):
        data = self.gui.make_request({
            "request_type": "spectrogram",
            "source": "microphone",
            "blocksize": self.blocksize,
            "return_raw_data": True,
        })
        data = data.mean(axis=1) * 10
        data = abs(np.fft.fft(data))[self.r1:self.r2]
        return data

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