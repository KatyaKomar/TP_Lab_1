from collections import namedtuple

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton, QRadioButton, QVBoxLayout, QLabel, QWidget, QColorDialog, QFileDialog, \
    QButtonGroup, QInputDialog

from helpers.constants import (
    DefaultSideBarParams as SideBarParams,
    DefaultColorButtonParams,
    ButtonsTitles, ButtonsLabels, PaintMode)
from helpers.mappings import (
    FIGURE_LABEL_MAPPINGS,
    SEVERAL_POINTS_FIGURES_LABEL,
    PAINT_MODE_MAPPING
)

DialogParams = namedtuple(
    'DialogParams',
    [
        'min_points_num',
        'dialog_point_step'
    ]
)


class SideBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent            # MainWindow instance
        self.parent.active = None       # active figure
        self.parent.paint_mode = None

        self.figures_radio_buttons = []
        self.paint_mode_radio_buttons = []

        self.num_btn = QPushButton(ButtonsLabels.set_num, self)
        self.reset_btn = QPushButton(ButtonsLabels.reset, self)
        self.border_color_btn = QColorButton(ButtonsLabels.border_color)
        self.bg_color_btn = QColorButton(ButtonsLabels.bg_color)

        self.choose_paint_mode_btn_group = QButtonGroup()
        self.choose_figure_btn_group = QButtonGroup()

        self.set_bg_color()
        self.render_buttons()

    def render_buttons(self):
        layout = QVBoxLayout()
        layout.setAlignment(SideBarParams.alignment)
        layout.setContentsMargins(
            SideBarParams.margin_left,
            SideBarParams.margin_top,
            SideBarParams.margin_right,
            SideBarParams.margin_bottom,
        )

        layout.addWidget(self.reset_btn)
        self.reset_btn.clicked.connect(lambda: self.parent.draw_area.reset())

        layout.addWidget(self.num_btn)
        self.num_btn.clicked.connect(lambda: self.show_dialog(self.parent.active))

        layout.addWidget(QLabel(ButtonsTitles.border_color, self))
        layout.addWidget(self.border_color_btn)

        layout.addWidget(QLabel(ButtonsTitles.bg_color, self))
        layout.addWidget(self.bg_color_btn)

        layout.addWidget(QLabel(ButtonsTitles.figure, self))
        self.render_choose_figure_btns(layout)

        layout.addWidget(QLabel(ButtonsTitles.paint_mode, self))
        self.render_paint_mode_btns(layout)

        self.setLayout(layout)

    def render_choose_figure_btns(self, layout):
        # render buttons to choose a figure
        self.figures_radio_buttons = [
            QRadioButton(figure_label)
            for figure_label in FIGURE_LABEL_MAPPINGS.keys()
        ]

        for button in self.figures_radio_buttons:
            layout.addWidget(button)

        for button in self.figures_radio_buttons:
            self.choose_figure_btn_group.addButton(button)

        # set processing function
        self.choose_figure_btn_group.buttonClicked[int].connect(
            self.choose_figure_btns_processor
        )

        # set first active figure as default
        self.figures_radio_buttons[0].setChecked(True)
        self.parent.active = self.figures_radio_buttons[0].text()
        self.parent.num = 3

    def choose_figure_btns_processor(self, button_id):
        for button in self.choose_figure_btn_group.buttons():
            if button is self.choose_figure_btn_group.button(button_id):
                self.show_dialog(button.text())
                self.parent.active = button.text()
                self.paint_mode_radio_buttons[0].setChecked(True)
                self.parent.paint_mode = PaintMode.draw
                self.parent.draw_area.points = []

    def render_paint_mode_btns(self, layout):
        # render buttons to choose a paint mode
        self.paint_mode_radio_buttons = [
            QRadioButton(label)
            for label in [ButtonsLabels.draw, ButtonsLabels.move]
        ]

        for button in self.paint_mode_radio_buttons:
            layout.addWidget(button)

        for button in self.paint_mode_radio_buttons:
            self.choose_paint_mode_btn_group.addButton(button)

        # set processing function
        self.choose_paint_mode_btn_group.buttonClicked[int].connect(
            self.choose_paint_mode_btns_processor
        )

        # set 'draw' paint mode as default
        self.paint_mode_radio_buttons[0].setChecked(True)
        self.parent.paint_mode = PaintMode.draw

    def choose_paint_mode_btns_processor(self, button_id):
        for button in self.choose_paint_mode_btn_group.buttons():
            if button is self.choose_paint_mode_btn_group.button(button_id):
                new_paint_mode = PAINT_MODE_MAPPING.get(button.text())
                if new_paint_mode:
                    self.parent.paint_mode = new_paint_mode
                    self.parent.draw_area.points = []

    def set_bg_color(self):
        color = SideBarParams.bg_color
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
        self.setAutoFillBackground(True)

    def show_dialog(self, active_name):
        dialog_params = DialogParams(3, 1)

        if active_name in SEVERAL_POINTS_FIGURES_LABEL:
            num, _ = QInputDialog.getInt(
                self,
                'points dialog',
                'enter a number of points',
                min=dialog_params.min_points_num,
                step=dialog_params.dialog_point_step,
                value=dialog_params.min_points_num,
            )
            self.parent.num = num


class QColorButton(QPushButton):
    '''
    Custom Qt Widget to show a chosen color.
    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    '''

    colorChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QColorButton, self).__init__(*args, **kwargs)

        self._color = None
        self.setMaximumWidth(DefaultColorButtonParams.width)
        self.pressed.connect(self.on_color_picker)

    def set_color(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit()

        if self._color:
            self.setStyleSheet("background-color: %s;"%self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return QColor(self._color)

    def on_color_picker(self):
        '''
        Show color-picker dialog to select color.
        Qt will use the native dialog by default.
        '''
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec_():
            self.set_color(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.set_color(None)

        return super(QColorButton, self).mousePressEvent(e)