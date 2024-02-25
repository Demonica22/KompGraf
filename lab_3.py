import sys
import matplotlib
from PyQt5 import uic, QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import math

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.size = 20

        uic.loadUi('ui_forms/third.ui', self)
        self.setMinimumSize(QtCore.QSize(800, 200))
        self.canvas = MplCanvas(self, width=5, height=5, dpi=100)
        self.verticalLayout.addWidget(self.canvas)

        self.draw_button.clicked.connect(self.draw)
        self.show()

    @property
    def points(self):
        points = []
        for i in range(1, 5):
            points.append(
                [self.__dict__[f'x_{i}'].value(), self.__dict__[f'y_{i}'].value(), self.__dict__[f'z_{i}'].value()])
        return points

    def draw(self):
        try:
            self.canvas.axes.cla()

            angle_x, angle_y = self.angle_x.value() * math.pi / 180, self.angle_y.value() * math.pi / 180
            corner_points = np.array(self.points)

            # Матрицы поворота
            rotation_matrix_x = np.array([[1, 0, 0],
                                          [0, np.cos(angle_x), -np.sin(angle_x)],
                                          [0, np.sin(angle_x), np.cos(angle_x)]])

            rotation_matrix_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                                          [0, 1, 0],
                                          [-np.sin(angle_y), 0, np.cos(angle_y)]])

            # Поворачиваем угловые точки
            corner_points = np.dot(rotation_matrix_x, corner_points.T).T
            corner_points = np.dot(rotation_matrix_y, corner_points.T).T

            # Определяем размер сетки для более плавного отображения
            grid_size = 50
            x = np.linspace(0, 1, grid_size)
            y = np.linspace(0, 1, grid_size)
            x, y = np.meshgrid(x, y)

            # Создаем пустую 2D-плоскость для координат Z
            z = np.zeros_like(x)

            # Вычисляем координаты Z по уравнению билинейной поверхности
            for i in range(grid_size):
                for j in range(grid_size):
                    xi = x[i, j]
                    yj = y[i, j]
                    z[i, j] = (1 - xi) * (1 - yj) * corner_points[0, 2] + \
                              xi * (1 - yj) * corner_points[1, 2] + \
                              (1 - xi) * yj * corner_points[2, 2] + \
                              xi * yj * corner_points[3, 2]

            # Создаем объект Figure и 3D-подграфик
            # Строим билинейную поверхность
            self.canvas.axes.plot_surface(x, y, z, cmap='viridis')

            # Поворачиваем поверхность относительно осей X и Y
            self.canvas.axes.view_init(30, 30)  # Углы обзора (30 градусов по оси X, 30 градусов по оси Y)
            self.canvas.axes.set_xlabel("X", fontweight='bold')
            self.canvas.axes.set_ylabel("Y", fontweight='bold')
            self.canvas.axes.set_zlabel("Z", fontweight='bold')

            # Отображаем график
            self.canvas.draw()
        except Exception as x:
            print(x)


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
