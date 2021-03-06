#######################################################
# 
# Line.py
# Python implementation of the Class Line
# Generated by Enterprise Architect
# Created on:      17-���-2021 17:53:23
# Original author: User
# 
#######################################################
from shapes.Ray import Ray
from helpers.geometry import get_line_point


class Line(Ray):

    def __init__(self, start_point, end_point, border_color, border):
        super().__init__(
            start_point=get_line_point(start_point, end_point, x=0.001),
            end_point=end_point,
            border_color=border_color,
            border=border
        )
