#######################################################
# 
# Circle.py
# Python implementation of the Class Circle
# Generated by Enterprise Architect
# Created on:      17-���-2021 17:52:44
# Original author: User
# 
#######################################################
from PyQt5.QtCore import QPoint

from shapes.Ellipse import Ellipse
from helpers.geometry import get_distance


class Circle(Ellipse):

    def __init__(self, border_color, inner_color, center_point, border_point):
        super().__init__(
            center_point=center_point,
            border_color=border_color,
            inner_color=inner_color,
            left_point=QPoint(border_point.x(), border_point.y()),
            top_point=QPoint(border_point.x(), border_point.y())
        )

    def draw(self, qp):
        qp.setPen(self.pen)
        qp.setBrush(self._inner_color)
        radius = get_distance(self._center_point, self._left_point)
        qp.drawEllipse(self._center_point, radius, radius)
