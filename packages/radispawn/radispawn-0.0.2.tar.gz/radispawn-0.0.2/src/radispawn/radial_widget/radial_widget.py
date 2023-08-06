import sys
from subprocess import Popen

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import QRect, Qt

class Wedge:
    def __init__(self, label, call, r, g, b):
        self.label = label
        self.color = QColor.fromRgb(r, g, b)
        self.call = call

class RadialMenu(QWidget):
    def __init__(self, wedges, outer_radius=200, inner_radius=100, select_color=0x000000, select_width=10):
        QWidget.__init__(self)

        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.select_color = select_color
        self.select_width = select_width
        self.wedges = wedges
        self.selected_wedge = 0

        # Needs to extend to the edge of the border around the outer radius
        self.resize((self.outer_radius + self.select_width) * 2, (self.outer_radius + self.select_width) * 2)
        self.setMinimumSize((self.outer_radius + self.select_width) * 2, (self.outer_radius + self.select_width) * 2)

        # Required for keyboard inputs
        self.setEnabled(True)
        self.grabKeyboard()

    # Select the next wedge clockwise
    def nextWedge(self):
        self.selected_wedge -= 1
        if self.selected_wedge < 0:
            self.selected_wedge += len(self.wedges)
        self.update()
    
    # Select the next wedge counterclockwise
    def prevWedge(self):
        self.selected_wedge += 1
        if self.selected_wedge == len(self.wedges):
            self.selected_wedge = 0
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Right:
            self.nextWedge()
        elif key == Qt.Key_Left:
            self.prevWedge()
        elif key == Qt.Key_Return:
            Popen(self.wedges[self.selected_wedge].call.split())
            sys.exit(0)
        else:
            sys.exit(0)

    def paintEvent(self, event):
        # Angle of each wedge
        angle = 360 * 16 / len(self.wedges)
        # Angle of the right edge of the first wedge
        base_angle = 90 * 16 - angle / 2

        painter = QPainter()
        painter.begin(self)

        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw wedges as pie slices
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        for idx, wedge in enumerate(self.wedges):
            painter.setBrush(QBrush(wedge.color))
            # Extend from a distance from the edge that enables the selection border to be visible
            painter.drawPie(self.select_width, self.select_width, self.outer_radius * 2, self.outer_radius * 2, base_angle + angle * idx, angle)

        # Erase center of donut
        painter.setCompositionMode(QPainter.CompositionMode_DestinationOut)
        # Center is outer + sel_wid, so corners are that +/- inner
        painter.drawEllipse(self.outer_radius - self.inner_radius + self.select_width, self.outer_radius - self.inner_radius + self.select_width, self.inner_radius * 2, self.inner_radius * 2)

        # Draw border, same logic as the drawPie call above
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        pen = QPen(self.select_color)
        pen.setWidth(self.select_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawArc(self.select_width, self.select_width, self.outer_radius * 2, self.outer_radius * 2, base_angle + angle * self.selected_wedge, angle)

        painter.end()
