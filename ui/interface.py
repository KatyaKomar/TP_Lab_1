from PyQt5.QtWidgets import QMainWindow

from helpers.constants import (
    DefaultMainWindowParams as WinParams,
    DefaultSideBarParams as SideBarParams,
)
from ui.draw import DrawArea
from ui.widgets import SideBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.draw_area = DrawArea(self)
        self.sidebar = SideBar(self)
        self._render_window_items()

    def _render_window_items(self):
        self.setWindowTitle(WinParams.title)
        # set Window params
        self.setGeometry(
            WinParams.left_indent,
            WinParams.top_indent,
            WinParams.width,
            WinParams.height,
        )
        self.setFixedSize(self.size())

        # should be set explicitly in constants
        width = SideBarParams.width

        # self.size().height() method returns the height of the MainWindow
        height = SideBarParams.height or self.size().height()

        # resize the sidebar and move it to the right side
        self.sidebar.resize(width, height)
        self.sidebar.move(self.size().width() - width, 0)

        # draw area settings
        self.draw_area.move(0, 0)
        self.draw_area.resize(self.size())

        self.show()
