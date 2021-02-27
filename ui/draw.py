from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QMessageBox

from helpers.constants import COMMON_ERROR_MSG, PAINT_ERROR_MSG, PaintMode, FigureLabels
from helpers.geometry import get_distance
from shapes.BrokenLine import BrokenLine
from shapes.Circle import Circle
from shapes.Ellipse import Ellipse
from shapes.Line import Line
from shapes.LineSegment import LineSegment
from shapes.Polygon import Polygon
from shapes.Ray import Ray
from shapes.RegularPolygon import RegularPolygon


class DrawArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setToolTip('This is a Draw Area!')
        self.reset()
        self.show()

    def reset(self):
        self.figure_to_move = None
        self.points = []
        self.figures = []
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_points(qp)
        self.draw_figures(qp)
        qp.end()

    def draw_points(self, qp):
        pen = QPen(Qt.red)
        pen.setCapStyle(Qt.RoundCap)
        pen.setWidth(5)
        qp.setPen(pen)

        for point in self.points:
            qp.drawPoint(point)

    def draw_figures(self, qp):
        for fig in self.figures:
            fig.draw(qp)

    def __is_enough_points(self, trigger_value):
        return len(self.points) == trigger_value

    def _section_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(2):
            figure = LineSegment(
                border_color=kwargs.get('border_color'),
                start_point=self.points[0],
                end_point=self.points[1]
            )
        return figure

    def _ray_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(2):
            figure = Ray(
                border_color=kwargs.get('border_color'),
                start_point=self.points[0],
                end_point=self.points[1],
                border=self.geometry(),
            )
        return figure

    def _line_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(2):
            figure = Line(
                border_color=kwargs.get('border_color'),
                start_point=self.points[0],
                end_point=self.points[1],
                border=self.geometry(),
            )
        return figure

    def _circle_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(2):
            figure = Circle(
                border_color=kwargs.get('border_color'),
                inner_color=kwargs.get('inner_color'),
                center_point=self.points[0],
                border_point=self.points[1]
            )
        return figure

    def _ellipse_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(3):
            figure = Ellipse(
                border_color=kwargs.get('border_color'),
                inner_color=kwargs.get('inner_color'),
                center_point=self.points[0],
                left_point=self.points[1],
                top_point=self.points[2],
            )
        return figure

    def _broken_line_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(self.parent.num):
            figure = BrokenLine(
                border_color=kwargs.get('border_color'),
                inner_points=self.points,
            )
        return figure

    def _polygon_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(self.parent.num):
            figure = Polygon(
                border_color=kwargs.get('border_color'),
                inner_color=kwargs.get('inner_color'),
                border_points=self.points,
            )
        return figure

    def _regular_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(2):
            figure = RegularPolygon(
                border_color=kwargs.get('border_color'),
                inner_color=kwargs.get('inner_color'),
                center_point=self.points[0],
                border_point=self.points[1],
                num=self.parent.num
            )
        return figure

    def _triangle_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(3):
            figure = Polygon(
                border_color=kwargs.get('border_color'),
                inner_color=kwargs.get('inner_color'),
                border_points=self.points,
            )
        return figure

    def _quadrilateral_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(4):
            figure = Polygon(
                border_color=kwargs.get('border_color'),
                inner_color=kwargs.get('inner_color'),
                border_points=self.points,
            )
        return figure

    def _rectangle_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(2):
            fir, sec = self.points
            figure = Polygon(
                border_color=kwargs.get('border_color'),
                inner_color=kwargs.get('inner_color'),
                border_points=[
                    fir, QPoint(fir.x(), sec.y()),
                    sec, QPoint(sec.x(), fir.y())
                ]
            )
        return figure

    def _rhombus_processor(self, **kwargs):
        figure = None
        if self.__is_enough_points(2):
            fir, sec = self.points
            figure = Polygon(
                border_color=kwargs.get('border_color'),
                inner_color=kwargs.get('inner_color'),
                border_points=[
                    fir, sec,
                    QPoint(fir.x(), 2 * sec.y() - fir.y()),
                    QPoint(2 * fir.x() - sec.x(), sec.y())
                ]
            )
        return figure

    def _new_figure_event_processor(self):
        # remove all auxiliary points from the screen
        self.points = []
        # perform screen update
        self.update()

    @property
    def border_color(self):
        return self.parent.sidebar.border_color_btn.color()

    @property
    def inner_color(self):
        return self.parent.sidebar.bg_color_btn.color()

    def _draw_figure(self, event):
        figure_processor_mappings = {
            FigureLabels.section_label: self._section_processor,
            FigureLabels.line_label: self._line_processor,
            FigureLabels.ray_label: self._ray_processor,
            FigureLabels.broken_line_label: self._broken_line_processor,
            FigureLabels.regular_polygon_label: self._regular_processor,
            FigureLabels.polygon_label: self._polygon_processor,
            FigureLabels.circle_label: self._circle_processor,
            FigureLabels.ellipse_label: self._ellipse_processor,
            FigureLabels.triangle_label: self._triangle_processor,
            FigureLabels.rectangle_label: self._rectangle_processor,
            FigureLabels.rhombus_label: self._rhombus_processor,
            FigureLabels.quadrilateral_label: self._quadrilateral_processor,
        }

        # save new point
        self.points.append(event.pos())
        # display new point on the screen
        self.update()

        figure_processor = figure_processor_mappings.get(self.parent.active)

        if figure_processor is None:
            raise KeyError(PAINT_ERROR_MSG)

        try:
            figure = figure_processor(
                border_color=self.border_color,
                inner_color=self.inner_color,
            )
            if figure:
                self.figures.append(figure)
                # drawing is happening here
                self._new_figure_event_processor()
        except:
            raise Exception(COMMON_ERROR_MSG)

    def __select_nearest_figure(self, event_point: QPoint):
        result_distance = float('inf')
        result_figure = None
        for figure in self.figures:
            distance = get_distance(figure.center_point, event_point)
            if distance < result_distance:
                result_distance = distance
                result_figure = figure
        return result_figure

    def _move_figure(self, event):
        self.points.append(event.pos())

        if self.__is_enough_points(1) and self.figures:
            # use a new point to select figure
            self.figure_to_move = self.__select_nearest_figure(self.points[0])

        elif self.__is_enough_points(2) and self.figures:
            # repopulate all figure points
            new_center = self.points[1]
            shift_vector = QPoint(
                new_center.x() - self.figure_to_move.center_point.x(),
                new_center.y() - self.figure_to_move.center_point.y(),
            )
            self.figure_to_move.move(shift_vector)
            # redraw figures
            self._new_figure_event_processor()

    def mousePressEvent(self, event):
        # entry point for all paint event
        mode_processors_mapping = {
            PaintMode.move: self._move_figure,
            PaintMode.draw: self._draw_figure,
        }
        try:
            processor = mode_processors_mapping.get(self.parent.paint_mode)
            processor(event)
        except Exception as exc:
            self.points = []
            self._show_error_msg(exc)

    @staticmethod
    def _show_error_msg(exc):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Ooops!!!')
        msg.setInformativeText(f'{exc}')
        msg.exec_()
