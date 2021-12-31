import sys
from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np
import time
from matplotlib import cm


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)

        # self.graphWidget = pg.PlotWidget()
        # self.setCentralWidget(self.graphWidget)

        self.data = data
        # self.fig = self.image(data)
        self.fig = pg.image(data)
        self.fig.setColorMap(pg.colormap.get("plasma"))
        # self.bar = pg.ColorBarItem(colorMap="jet")
        # self.bar.setImageItem()

        self.timer = pg.Qt.QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def image(self, data):
        return self.graphWidget.image(data)

    def update_plot_data(self):
        shape = self.data.shape
        self.data = self.data[:, 1:]

        new_col = np.random.uniform(size=(shape[0], 1))
        self.data = np.hstack((self.data, new_col))

        self.fig.setImage(self.data.T)


def main():
    app = QtWidgets.QApplication(sys.argv)

    data = np.random.uniform(size=(50, 50))

    main = MainWindow(data)
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
