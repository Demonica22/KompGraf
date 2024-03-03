import math
import sys
import matplotlib
from PyQt5 import uic, QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as pyplot
from matplotlib.patches import Polygon
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.size = 100

        uic.loadUi('ui_forms/fourth.ui', self)
        self.setMinimumSize(QtCore.QSize(800, 200))
        self.canvas = MplCanvas(self, width=5, height=5, dpi=100)
        self.verticalLayout.addWidget(self.canvas)
        self.canvas.axes.set_ylim(-self.size, self.size)
        self.canvas.axes.set_xlim(-self.size, self.size)
        self.polygon = [(20, 20), (40, 10), (60, 20), (60, 40), (40, 50), (20, 40)]
        self.window_coords = [(32, 32), (52, 32), (52, 47), (32, 47)]
        self.update_points()

        self.pushButton_2.clicked.connect(self.add_point)
        self.pushButton_3.clicked.connect(self.delete_point)
        self.pushButton_5.clicked.connect(self.change_point_coords)

        self.spinBox_6.valueChanged.connect(self.load_point_coords)

        self.pushButton.clicked.connect(self.draw)
        self.show()

    def draw(self):
        try:
            self.canvas.axes.cla()
            clipped_polygon = self.clip_polygon(self.polygon, self.window_coords)
            origin = Polygon(self.polygon, facecolor="green",edgecolor="green")
            poly = Polygon(clipped_polygon, facecolor='blue', edgecolor='blue')
            window = Polygon(self.window_coords, facecolor='none', edgecolor='red')
            self.canvas.axes.add_patch(origin)
            self.canvas.axes.add_patch(poly)
            self.canvas.axes.add_patch(window)
            self.canvas.axes.set_ylim(0, self.size)
            self.canvas.axes.set_xlim(0, self.size)
            self.canvas.draw()
        except Exception as x:
            print(x)

    def clip_polygon(self, polygon, window):
        output = polygon.copy()
        for i in range(len(window)):
            input = output.copy()
            output.clear()
            s = input[-1]
            for j in range(len(input)):
                p = input[j]
                if self.get_side(window[i], window[(i + 1) % len(window)], p) >= 0:
                    if self.get_side(window[i], window[(i + 1) % len(window)], s) < 0:
                        intersection = [
                            s[0] + (p[0] - s[0]) * (self.get_side(window[i], window[(i + 1) % len(window)], s) / (
                                        self.get_side(window[i], window[(i + 1) % len(window)], s) - self.get_side(window[i],
                                                                                                         window[(
                                                                                                                            i + 1) % len(
                                                                                                             window)],
                                                                                                         p))),
                            s[1] + (p[1] - s[1]) * (self.get_side(window[i], window[(i + 1) % len(window)], s) / (
                                        self.get_side(window[i], window[(i + 1) % len(window)], s) - self.get_side(window[i],
                                                                                                         window[(
                                                                                                                            i + 1) % len(
                                                                                                             window)],
                                                                                                         p)))
                        ]
                        output.append(intersection)
                    output.append(p)
                elif self.get_side(window[i], window[(i + 1) % len(window)], s) >= 0:
                    intersection = [
                        s[0] + (p[0] - s[0]) * (self.get_side(window[i], window[(i + 1) % len(window)], s) / (
                                    self.get_side(window[i], window[(i + 1) % len(window)], s) - self.get_side(window[i], window[
                                (i + 1) % len(window)], p))),
                        s[1] + (p[1] - s[1]) * (self.get_side(window[i], window[(i + 1) % len(window)], s) / (
                                    self.get_side(window[i], window[(i + 1) % len(window)], s) - self.get_side(window[i], window[
                                (i + 1) % len(window)], p)))
                    ]
                    output.append(intersection)
                s = p
        return output
    def get_side(self, p1, p2, p):
        return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0])

    def update_points(self):
        self.label_2.setText("\n".join([f"({point[0]};{point[1]})" for point in self.window_coords]))
    def load_point_coords(self, point_index):
        self.spinBox_2.setValue(self.window_coords[point_index-1][0])
        self.spinBox_5.setValue(self.window_coords[point_index-1][1])

    def change_point_coords(self):
        self.window_coords[self.spinBox_6.value()-1] = (self.spinBox_2.value(), self.spinBox_5.value())
        self.update_points()
    def add_point(self):
        x, y = self.spinBox.value(), self.spinBox_3.value()
        if (x, y) not in self.window_coords:
            self.window_coords.append((x, y))
        self.update_points()
        self.spinBox_6.setMaximum = len(self.window_coords)

    def delete_point(self):
        if self.window_coords:
            self.window_coords.pop(-1)
            self.update_points()
        self.spinBox_6.setMaximum = len(self.window_coords)

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
