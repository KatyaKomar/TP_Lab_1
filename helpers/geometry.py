import numpy as np
from math import hypot
from PyQt5.QtCore import QPoint


def midpoint(p1: QPoint, p2: QPoint) -> QPoint:
    """
    Calculate the center point between two points.
    NOTE: center = ( (x1+x2)/2, (y1+y2)/2 )
    """
    return QPoint((p1.x() + p2.x())/2, (p1.y() + p2.y())/2)


def get_line_point(p1: QPoint, p2: QPoint, x=None, y=None) -> QPoint:
    """
    Compute the coefficients of the line y = a*x + b
    that connects the two points using the polyfit method from numpy.
    And after that, if x is set, then compute y coordinate, otherwise calculate x
    :param p1: First known line point
    :param p2: Second known line point
    :param x:  Known x coordinate (if x is unknown, then x param is None)
    :param y:  Known y coordinate (if y is unknown, then y param is None
    :return:   Needed point
    """
    x_list, y_list = [p1.x(), p2.x()], [p1.y(), p2.y()]
    a, b = np.polyfit(x_list, y_list, 1)
    if x is not None:
        y = a*x + b
    elif y is not None:
        x = (y - b)/a
    return QPoint(x, y)


def get_distance(p1: QPoint, p2: QPoint):
    """Compute and return distance between two points"""
    return hypot(p1.x() - p2.x(), p1.y() - p2.y())