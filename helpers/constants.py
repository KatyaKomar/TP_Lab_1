from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

PAINT_ERROR_MSG = "Ooops, something is wrong with our paint app. We are fixing this error now ;)"
COMMON_ERROR_MSG = "Unexpected error. Even we don't know what has happened. Try again)"


class DefaultMainWindowParams:
    title = "Paint Application"
    left_indent = 600
    top_indent = 200
    width = 1000
    height = 700


class DefaultSideBarParams:
    bg_color = QColor('lightgray')
    width = 200
    height = None
    margin_left = 10
    margin_top = 40
    margin_right = 10
    margin_bottom = 30
    alignment = Qt.AlignTop


class ButtonsLabels:
    set_num = 'Set num'
    reset = 'Reset'
    border_color = 'Choose border color'
    bg_color = 'Choose background color'
    move = 'Move figure'
    draw = 'Draw figure'


class ButtonsTitles:
    bg_color = 'Bg color:'
    border_color = 'Border color:'
    figure = 'Figure:'
    paint_mode = 'Select paint mode:'


class DefaultColorButtonParams:
    width = 200
    height = None


class DefaultDrawParams:
    pen_color = Qt.black
    pen_style = Qt.SolidLine
    pen_cap_style = Qt.RoundCap
    pen_join_style = Qt.RoundJoin
    pen_thickness = 3
    inner_color = Qt.white


class PaintMode:
    draw = 'paint'
    move = 'move'


class FigureLabels:
    circle_label = 'circle'
    ellipse_label = 'ellipse'
    line_label = 'line'
    broken_line_label = 'broken line'
    ray_label = 'ray'
    section_label = 'section'
    regular_polygon_label = 'regular polygon'
    polygon_label = 'polygon'
    triangle_label = 'triangle'
    rhombus_label = 'rhombus'
    rectangle_label = 'rectangle'
    quadrilateral_label = 'quadrilateral'
