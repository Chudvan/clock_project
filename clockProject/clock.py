from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QTimer

from PyQt5.QtGui import QColor

import math
import datetime

class Clock(QWidget):
    def __init__(self, timezone=None, mode=None, h=None, m=None, s=None):
        super().__init__()

        self.qp = QPainter()

        if (h is not None and m is not None and s is not None):
            self.h = h
            self.m = m
            self.s = s
        else:
            self.init_time(timezone)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

        self.mode = mode

        self.update()


    def init_time(self, timezone):
        now = datetime.datetime.utcnow()

        if timezone is not None:
            self.h = now.hour + timezone
        else:
            self.h = now.hour

        self.m = now.minute
        self.s = now.second


    def draw_dial(self):
        for i in range(60):
            angle = math.pi / 2 - math.pi / 30 * i

            if (i % 5 == 0):
                coor1 = [int(self.centr[0] + 0.43 * self.diam * math.cos(angle)), int(self.centr[1] - 0.43 * self.diam * math.sin(angle))]
            else:
                coor1 = [int(self.centr[0] + 0.47 * self.diam * math.cos(angle)), int(self.centr[1] - 0.47 * self.diam * math.sin(angle))]

            coor2 = [int(self.centr[0] + 0.5 * self.diam * math.cos(angle)), int(self.centr[1] - 0.5 * self.diam * math.sin(angle))]

            self.qp.drawLine(*coor1, *coor2)


    def update_angles(self):
        h_angle = math.pi / 2 - math.pi / 6 * self.h - math.pi * self.m / 360
        m_angle = math.pi / 2 - math.pi / 30 * self.m
        s_angle = math.pi / 2 - math.pi / 30 * self.s

        self.h_coord = [int(self.centr[0] + self.h_len * math.cos(h_angle)), int(self.centr[1] - self.h_len * math.sin(h_angle))]
        self.m_coord = [int(self.centr[0] + self.m_len * math.cos(m_angle)), int(self.centr[1] - self.m_len * math.sin(m_angle))]
        self.s_coord = [int(self.centr[0] + self.s_len * math.cos(s_angle)), int(self.centr[1] - self.s_len * math.sin(s_angle))]


    def paintEvent(self, event):
        self.update_angles()

        self.qp.begin(self)

        self.draw_dial()
        self.draw_arrows()

        self.qp.end()


    def draw_arrows(self):
        self.qp.setPen(QColor(0, 0, 0))
        self.qp.drawLine(*self.centr, *self.h_coord)
        self.qp.drawLine(*self.centr, *self.m_coord)

        self.qp.setPen(QColor(255, 0, 0))
        self.qp.drawLine(*self.centr, *self.s_coord)


    def resizeEvent(self, event):
        self.diam = min(self.size().width(), self.size().height())

        self.h_len = 0.2 * self.diam
        self.m_len = 0.3 * self.diam
        self.s_len = 0.4 * self.diam

        self.centr = [int(self.size().width() / 2), int(self.size().height() / 2)]


    def tick(self):
        if (self.mode == 1):
            self.s += 1

            if (self.s == 60):
                self.m += 1
                self.s = 0

            if (self.m == 60):
                self.h += 1
                self.m = 0

            if (self.h == 24):
                self.h = 0
        else:
            self.s -= 1

            if (self.s < 0):
                self.m -= 1
                self.s = 59

            if (self.m < 0):
                self.h -= 1
                self.m = 59

            if (self.h < 0):
                self.h = 23

            if (self.h == 0) and (self.m == 0) and (self.s == 0):
                self.timer.stop()

        self.update()