import math
import sys
import matplotlib
from PyQt5 import uic, QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as pyplot

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


def make_bezier(points):
    n = len(points)
    combinations = pascal_row(n - 1)

    def bezier(ts):
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t ** i for i in range(n))
            upowers = reversed([(1 - t) ** i for i in range(n)])
            coefficients = [c * a * b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(tuple(sum([coefficient * p for coefficient, p in zip(coefficients, ps)]) for ps in zip(*points)))
        return result

    return bezier


def pascal_row(n, memory={}):
    # Функция просчитывает n-ый ряд треугольника Паскаля (коэффициенты полинома)
    # Так же кеширует заранее просчитанные значения с помощью словаря - memory. Для ускорения работы
    if n in memory:
        return memory[n]
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n // 2 + 1):
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n % 2 == 0:
        # n - четное
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    memory[n] = result
    return result


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.size = 20

        uic.loadUi('ui_forms/second.ui', self)
        self.setMinimumSize(QtCore.QSize(800, 200))
        self.canvas = MplCanvas(self, width=5, height=5, dpi=100)
        self.verticalLayout.addWidget(self.canvas)
        self.canvas.axes.set_ylim(-self.size, self.size)
        self.canvas.axes.set_xlim(-self.size, self.size)
        self.points = [(0, 0), (-5, 10), (10, 10), (15, 0), (18, 5)]
        self.precision = 500
        self.update_points()
        self.pushButton.clicked.connect(self.draw)
        self.pushButton_2.clicked.connect(self.add_point)
        self.pushButton_3.clicked.connect(self.delete_point)
        self.show()

    def draw(self):
        try:
            self.canvas.axes.cla()

            self.precision = self.spinBox_4.value()
            if len(self.points):
                for i in range(len(self.points)-1):
                    self.canvas.axes.plot(self.points[i][0], self.points[i][1], 'ro', ms=3)
                    self.canvas.axes.plot([self.points[i][0],self.points[i+1][0]], [self.points[i][1], self.points[i+1][1]], 'red', lw=1)
                self.canvas.axes.plot(self.points[-1][0], self.points[-1][1], 'ro', ms=3)

                ts = [t / float(self.precision) for t in range(self.precision + 1)]

                bezier = make_bezier(self.points)
                points = bezier(ts)
                for point in points:
                    self.canvas.axes.plot(point[0], point[1], 'bo', ms=1)
            self.canvas.axes.set_ylim(-self.size, self.size)
            self.canvas.axes.set_xlim(-self.size, self.size)
            self.canvas.draw()
        except Exception as x:
            print(x)

    def update_points(self):
        self.label_2.setText("\n".join([f"({point[0]};{point[1]})" for point in self.points]))

    def add_point(self):
        x, y = self.spinBox.value(), self.spinBox_3.value()
        if (x, y) not in self.points:
            self.points.append((x, y))
        self.update_points()

    def delete_point(self):
        if self.points:
            self.points.pop(-1)
            self.update_points()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
