import numpy as np
from numpy.core.shape_base import block
import sounddevice as sd
import pyqtgraph as pg
from PyQt5 import QtWidgets
import time
import sys

from interface import GuiInterface
from chirper.transforms import fourier


# blocksize = 4410
# r1 = 0
# r2 = blocksize
# values = np.zeros((r2 - r1, r2 - r1))
# r1 = blocksize // 2
# r2 = 2 * blocksize // 3
# r2 = blocksize

# gui.make_request({
#     "request_type": "start",
#     "source": "microphone",
# })

# while True:
#     data = gui.make_request({
#         "request_type": "spectrogram",
#         "source": "microphone",
#         "blocksize": blocksize,
#         "return_raw_data": True,
#     })
#     data = data.mean(axis=1) * 10
#     data = abs(np.fft.fft(data))[r1:r2]
#     ax1 = np.vstack((ax1.T, data)).T

#     # print("|" * int(np.linalg.norm(data) * 10))

# gui.make_request({
#     "request_type": "stop",
#     "source": "microphone",
# })

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.gui = GuiInterface()
        # self.blocksize = 4410
        self.blocksize = 500
        # self.r1 = 0
        self.r1 = self.blocksize // 2
        # self.r2 = self.blocksize // 2
        self.r2 = self.blocksize
        # self.values = np.zeros((self.r2 - self.r1, self.r2 - self.r1))
        self.values = np.zeros((self.r2 - self.r1, self.blocksize // 2))

        # self.canvas = pg.GraphicsView()
        # self.vb = pg.ViewBox()
        # self.canvas.setCentralItem(self.vb)
        # self.vb.setAspectLocked()
        # self.canvas.show()

        self.fig = pg.image(self.values)
        # self.fig = pg.ImageItem(self.values)
        self.fig.setColorMap(pg.colormap.get("plasma"))
        # self.vb.addItem(self.fig)
        # self.fig.setCentralItem(self.vb)

        self.send_start_request()

        self.timer = pg.Qt.QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        # self.send_stop_request(self.gui)

    def image(self, data):
        return self.graphWidget.image(data)

    def update_plot_data(self):
        self.values = self.values[:, 1:]

        new_col = self.send_fetch_request()
        # new_col = np.random.uniform(size=(shape[0], 1))
        # self.values = np.hstack((self.values, new_col))
        self.values = np.vstack((self.values.T, new_col)).T

        self.fig.setImage(self.values.T)

    def send_start_request(self):
        self.gui.make_request({
            "request_type": "start",
            "source": "microphone",
        })

    def send_fetch_request(self):
        # while True:
        data = self.gui.make_request({
            "request_type": "spectrogram",
            "source": "microphone",
            "blocksize": self.blocksize,
            "return_raw_data": True,
        })
        data = data.mean(axis=1) * 10
        data = abs(np.fft.fft(data))[self.r1:self.r2]
        return data
        # self.values = np.vstack((self.values.T, data)).T

        # print("|" * int(np.linalg.norm(data) * 10))

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