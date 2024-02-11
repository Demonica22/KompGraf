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


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('ui_forms/first.ui', self)
        self.setMinimumSize(QtCore.QSize(800, 200))
        self.canvas = MplCanvas(self, width=5, height=5, dpi=100)
        self.verticalLayout.addWidget(self.canvas)
        self.canvas.axes.set_ylim(-50, 50)
        self.canvas.axes.set_xlim(-50, 50)

        self.pushButton.clicked.connect(self.draw)

        self.show()

    def get_data(self) -> dict:
        x_0 = self.spinBox.value()
        y_0 = self.spinBox_3.value()
        R = self.spinBox_2.value()
        x_1 = self.spinBox_5.value()
        y_1 = self.spinBox_6.value()
        return {"circle_centre": (x_0, y_0),
                "radius": R,
                "point": (x_1, y_1)}

    def draw(self):
        try:
            data = self.get_data()
            self.canvas.axes.cla()

            draw_circle = pyplot.Circle(data['circle_centre'], data['radius'], fill=False, color='red', linewidth=2)
            self.canvas.axes.plot(*data["point"], 'bo', ms=5)
            self.canvas.axes.add_artist(draw_circle)

            points = self.calculate_tangent_coords()
            for point in points:
                self.canvas.axes.plot([data['point'][0], point[0]], [data['point'][1], point[1]], 'black', lw=2)
                self.canvas.axes.plot(point[0], point[1], 'ro', ms=1)
            self.canvas.axes.set_ylim(-50, 50)
            self.canvas.axes.set_xlim(-50, 50)
            self.canvas.draw()
        except Exception as x:
            print(x)

    def calculate_tangent_coords(self):
        data = self.get_data()
        from_circle_centre_to_point = math.sqrt((data['point'][0] - data['circle_centre'][0]) ** 2 + (
                    data['point'][1] - data['circle_centre'][1]) ** 2)  # расстояние до центра окружности
        if from_circle_centre_to_point < data['radius']:
            print("ERROR: Radius is smaller than distance to point")
            self.label_8.setText("ERROR: \nРадиус меньше чем расстояние до точки.\nКасательные не построены")
            return []
        self.label_8.setText("")
        angle_lambda = math.acos(data['radius'] / from_circle_centre_to_point)  # Сдвиг угла, нужен для того, чтобы просчитать две точки касания (с двух сторон окружности)
        angle_from_point_to_centre = math.atan2(data['point'][1] - data['circle_centre'][1],
                                                data['point'][0] - data['circle_centre'][
                                                    0])  # угол прямой от заданной точки до центра окружности
        angle_of_tangent_1 = angle_from_point_to_centre + angle_lambda  # угол прямой от точки касания 1 до центра окружности
        angle_of_tangent_2 = angle_from_point_to_centre - angle_lambda  # угол прямой от точки касания 2 до центра окружности

        tangent_1_x = data['circle_centre'][0] + data['radius'] * math.cos(angle_of_tangent_1)
        tangent_1_y = data['circle_centre'][1] + data['radius'] * math.sin(angle_of_tangent_1)
        tangent_2_x = data['circle_centre'][0] + data['radius'] * math.cos(angle_of_tangent_2)
        tangent_2_y = data['circle_centre'][1] + data['radius'] * math.sin(angle_of_tangent_2)

        return (tangent_1_x, tangent_1_y), (tangent_2_x, tangent_2_y)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
