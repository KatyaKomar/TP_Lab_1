from helpers.constants import ButtonsLabels, PaintMode, FigureLabels
from shapes import (
    Circle,
    Ellipse,
    Line,
    BrokenLine,
    Ray,
    LineSegment,
    RegularPolygon,
    Polygon
)

PAINT_MODE_MAPPING = {
    ButtonsLabels.draw: PaintMode.draw,
    ButtonsLabels.move: PaintMode.move,
}

FIGURE_LABEL_MAPPINGS = {
    FigureLabels.circle_label: Circle,
    FigureLabels.ellipse_label: Ellipse,
    FigureLabels.line_label: Line,
    FigureLabels.broken_line_label: BrokenLine,
    FigureLabels.ray_label: Ray,
    FigureLabels.section_label: LineSegment,
    FigureLabels.regular_polygon_label: RegularPolygon,
    FigureLabels.polygon_label: Polygon,
    FigureLabels.triangle_label: Polygon,
    FigureLabels.rhombus_label: Polygon,
    FigureLabels.rectangle_label: Polygon,
    FigureLabels.quadrilateral_label: Polygon
}

SEVERAL_POINTS_FIGURES_LABEL = [
    FigureLabels.polygon_label,
    FigureLabels.broken_line_label,
    FigureLabels.regular_polygon_label,
]
