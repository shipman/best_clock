#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

# Steve modifications: we want a second hand!


from PyQt5.QtCore import QPoint, Qt, QTime, QTimer, pyqtSignal, QEvent
from PyQt5.QtGui import QColor, QPainter, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLCDNumber, QDialog
from functools import partial

import random
import math
import numpy
import sys
import copy
import pdb
import time

global real_time
global minotaur_standard_time

class BestClock(object):
    def setupUi(self):
        global real_time, minotaur_standard_time
        global Dialog

        Dialog.setObjectName("Dialog")
        Dialog.resize(375, 250)
        Dialog.setWindowTitle("Best Clock!!!1!!!1!")

        self.gridLayout = QGridLayout(Dialog)
        self.analog_part = AnalogClock()
        self.gridLayout.addWidget(self.analog_part, 0, 0, 1, 1)
        self.digital_part = DigitalClock()
        self.gridLayout.addWidget(self.digital_part, 1, 0, 1, 1)
        self.analog_MST_part = MSTAnalogClock()
        self.gridLayout.addWidget(self.analog_MST_part, 0, 1, 1, 1)
        self.digital_MST_part = MSTDigitalClock()
        self.gridLayout.addWidget(self.digital_MST_part, 1, 1, 1, 1)
        self.analog_MST_part.setAutoFillBackground(True)

        self.analog_MST_part.danger.connect(self.report_danger)

    def report_danger(self,value):
        global Dialog
        #print("I saw the sign and it opened up my eyes")
        p = Dialog.palette()
        #print("Value is %s"%value)

        direction = numpy.sign(random.uniform(-1.0,1.0))

        if value == 0:
            p.setColor(Dialog.backgroundRole(), QColor(255,255,255))
            Dialog.resize(375, 250)
            #Dialog.move(random.randrange(0,50)*direction,random.randrange(0,50)*direction)            

        if value == 1:
            p.setColor(Dialog.backgroundRole(), QColor(random.randrange(192,255),random.randrange(192,255),random.randrange(192,255)))
            Dialog.resize(375*random.uniform(0.75,1.33), 250*random.uniform(0.75,1.33))
            Dialog.move(random.randrange(0,50)*direction,random.randrange(0,50)*direction)

        elif value == 2:
            p.setColor(Dialog.backgroundRole(), QColor(random.randrange(128,191),random.randrange(128,191),random.randrange(128,191)))
            Dialog.resize(375*random.uniform(0.6,1.67), 250*random.uniform(0.6,1.67))
            Dialog.move(random.randrange(0,75)*direction,random.randrange(0,75)*direction)

        elif value == 3:
            p.setColor(Dialog.backgroundRole(), QColor(random.randrange(64,127),random.randrange(64,127),random.randrange(64,127)))
            Dialog.resize(375*random.uniform(0.9,1.1), 250*random.uniform(0.9,1.1))
            Dialog.move(random.randrange(0,100)*direction,random.randrange(0,100)*direction)

        elif value == 4:
            p.setColor(Dialog.backgroundRole(), QColor(random.randrange(0,63),random.randrange(0,63),random.randrange(0,63)))
            Dialog.resize(375*random.uniform(0.8,1.25), 250*random.uniform(0.8,1.25))
            Dialog.move(random.randrange(0,125)*direction,random.randrange(0,125)*direction)

        Dialog.setPalette(p)

class AnalogClock(QWidget):
    hourHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -40)
    ])

    minuteHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -70)
    ])

    secondHand = QPolygon([
        QPoint(1, 8),
        QPoint(-1, 8),
        QPoint(0, -100)])

    hourColor = QColor(127, 0, 127)
    minuteColor = QColor(0, 127, 127, 191)
    secondColor = QColor(255, 0, 0)

    def __init__(self, parent=None):
        super(AnalogClock, self).__init__(parent)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        #self.setWindowTitle("Analog Clock")
        self.resize(400, 400)
        self.setMouseTracking(True)

    def mouseMoveEvent(self,event):
        Dialog.move(300*random.uniform(0.0,1.0)*int(numpy.sign(random.uniform(-1.0,1.0))),300*random.uniform(0.0,1.0)*int(numpy.sign(random.uniform(-1.0,1.0))))

    def paintEvent(self, event):
        global real_time, minotaur_standard_time

        actual_time_updater()

        side = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.hourColor)

        painter.save()
        hour_adjust = 30.0 * ((int(real_time.hour) + int(real_time.minute) / 60.0))
        hour = math.floor(hour_adjust/30.0)
        painter.rotate(hour_adjust)
        painter.drawConvexPolygon(AnalogClock.hourHand)
        painter.restore()

        painter.setPen(AnalogClock.hourColor)

        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.minuteColor)

        painter.save()
        minute_adjust = 6.0 * ((int(real_time.minute) + int(real_time.second) / 60.0))
        if minute_adjust < 0:
            minute_adjust += 360
        minute = math.floor(minute_adjust/6.0)
        painter.rotate(minute_adjust)
        painter.drawConvexPolygon(AnalogClock.minuteHand)
        painter.restore()

        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.secondColor)

        painter.save()
        second_adjust = 6.0 * int(real_time.second)
        if second_adjust < 0:
            second_adjust += 360
        second = math.floor(second_adjust/6.0)
        painter.rotate(second_adjust)
        painter.drawConvexPolygon(AnalogClock.secondHand)
        painter.restore()

        painter.setPen(AnalogClock.minuteColor)

        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)

class MSTAnalogClock(QWidget):
    hourHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -40)
    ])

    minuteHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -70)
    ])

    secondHand = QPolygon([
        QPoint(1, 8),
        QPoint(-1, 8),
        QPoint(0, -100)])

    hourColor = QColor(127, 0, 127)
    minuteColor = QColor(0, 127, 127, 191)
    secondColor = QColor(255, 0, 0)



    def __init__(self, parent=None):
        super(MSTAnalogClock, self).__init__(parent)

        timer = QTimer(self)
        timer.timeout.connect(self.update_MST)
        timer.start(1000)

        self.setWindowTitle("Analog Clock")
        self.resize(400, 400)
        self.setMouseTracking(True)

    def mouseMoveEvent(self,event):
        Dialog.move(300*random.uniform(0.0,1.0)*int(numpy.sign(random.uniform(-1.0,1.0))),300*random.uniform(0.0,1.0)*int(numpy.sign(random.uniform(-1.0,1.0))))


    def paintEvent(self, event):
        global real_time, minotaur_standard_time

        side = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(MSTAnalogClock.hourColor)

        painter.save()
        hour_adjust = 30.0 * ((int(minotaur_standard_time.hour) + int(minotaur_standard_time.minute) / 60.0))
        hour = math.floor(hour_adjust/30.0)
        painter.rotate(hour_adjust)
        painter.drawConvexPolygon(MSTAnalogClock.hourHand)
        painter.restore()

        painter.setPen(MSTAnalogClock.hourColor)

        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(MSTAnalogClock.minuteColor)

        painter.save()
        minute_adjust = 6.0 * ((int(minotaur_standard_time.minute) + int(minotaur_standard_time.second) / 60.0))
        if minute_adjust < 0:
            minute_adjust += 360
        minute = math.floor(minute_adjust/6.0)
        painter.rotate(minute_adjust)
        painter.drawConvexPolygon(MSTAnalogClock.minuteHand)
        painter.restore()

        painter.setPen(Qt.NoPen)
        painter.setBrush(MSTAnalogClock.secondColor)

        painter.save()
        second_adjust = 6.0 * int(minotaur_standard_time.second)
        if second_adjust < 0:
            second_adjust += 360
        second = math.floor(second_adjust/6.0)
        painter.rotate(second_adjust)
        painter.drawConvexPolygon(MSTAnalogClock.secondHand)
        painter.restore()

        painter.setPen(MSTAnalogClock.minuteColor)

        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)

    danger = pyqtSignal(int)

    def update_MST(self):
        actual_time_updater()
        MST_time_updater()
        danger_level = proximity_alert()
        self.danger.emit(danger_level)


class DigitalClock(QLCDNumber):
    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)

        self.setSegmentStyle(QLCDNumber.Filled)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(0)

        self.showTime()

        self.setWindowTitle("Digital Clock")
        self.resize(150, 90)
        self.setDigitCount(8)
        self.setMouseTracking(True)

    def mouseMoveEvent(self,event):
        Dialog.move(300*random.uniform(0.0,1.0)*int(numpy.sign(random.uniform(-1.0,1.0))),300*random.uniform(0.0,1.0)*int(numpy.sign(random.uniform(-1.0,1.0))))

    def showTime(self):

        text = real_time.hour + ':' + real_time.minute + ':' + real_time.second

        self.display(text)

class MSTDigitalClock(QLCDNumber):
    def __init__(self, parent=None):
        super(MSTDigitalClock, self).__init__(parent)

        self.setSegmentStyle(QLCDNumber.Filled)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(0)

        self.showTime()

        self.setWindowTitle("Digital Clock")
        self.resize(150, 90)
        self.setDigitCount(8)
        self.setMouseTracking(True)

    def mouseMoveEvent(self,event):
        Dialog.move(300*random.uniform(0.0,1.0)*int(numpy.sign(random.uniform(-1.0,1.0))),300*random.uniform(0.0,1.0)*int(numpy.sign(random.uniform(-1.0,1.0))))

    def showTime(self):

        text = minotaur_standard_time.hour + ':' + minotaur_standard_time.minute + ':' + minotaur_standard_time.second

        chance = random.uniform(0.0,1.0)
        if chance < 0.02:
            text = "bEstkl0k"
            self.display(text)

        self.display(text)

def actual_time_updater():
    global real_time
    real_time.time = QTime.currentTime()
    real_time.string = real_time.time.toString('hh:mm:ss')
    real_time.hour = real_time.string[0:2]
    real_time.minute = real_time.string[3:5]
    real_time.second = real_time.string[6:8]

def MST_time_updater():
    global minotaur_standard_time
    delta_seconds = math.floor(minotaur_standard_time.state[2]*minotaur_standard_time.state[3]) #[2] is current direction, [3] is current speed

    if minotaur_standard_time.second[0] == "0":
        curr_second = int(minotaur_standard_time.second[1])
    else:
        curr_second = int(minotaur_standard_time.second)

    if minotaur_standard_time.minute[0] == "0":
        curr_minute = int(minotaur_standard_time.minute[1])
    else:
        curr_minute = int(minotaur_standard_time.minute)

    if minotaur_standard_time.hour[0] == "0":
        curr_hour = int(minotaur_standard_time.hour[1])
    else:
        curr_hour = int(minotaur_standard_time.hour)

    new_second = curr_second + delta_seconds
    new_minute = curr_minute
    new_hour = curr_hour

    while new_second >= 60: 
        new_minute += 1
        new_second = new_second - 60

    while new_second < 0:
        new_minute += -1
        new_second = new_second + 60

    while new_minute >= 60:
        new_hour += 1
        new_minute = new_minute - 60

    while new_minute < 0:
        new_hour += -1
        new_minute = new_minute + 60

    while new_hour >= 25:
        new_hour = new_hour - 24

    while new_hour < 0:
        new_hour += 24

    if new_second < 10:
        new_second_str = "0" + str(new_second)
    else:
        new_second_str = str(new_second)

    if new_minute < 10:
        new_minute_str = "0" + str(new_minute)
    else:
        new_minute_str = str(new_minute)

    if new_hour < 10:
        new_hour_str = "0" + str(new_hour)
    else:
        new_hour_str = str(new_hour)

    minotaur_standard_time.second = new_second_str
    minotaur_standard_time.minute = new_minute_str
    minotaur_standard_time.hour = new_hour_str

    minotaur_standard_time.state[0] = minotaur_standard_time.state[2]
    minotaur_standard_time.state[1] = minotaur_standard_time.state[3]
    minotaur_standard_time.state[2] = numpy.sign(random.uniform(-1.0,1.0)) # Need to make it more likely that time stops
    minotaur_standard_time.state[3] = random.uniform(0.0,2.0)


def time_initializer():
    r_time = QTime.currentTime()
    r_time.time = QTime.currentTime()
    r_time.string = r_time.time.toString('hh:mm:ss')
    r_time.hour = r_time.string[0:2]
    r_time.minute = r_time.string[3:5]
    r_time.second = r_time.string[6:8]
    return r_time

def proximity_alert():
    if minotaur_standard_time.hour[0] == "0":
        minotaur_hour = int(minotaur_standard_time.hour[1])
    else:
        minotaur_hour = int(minotaur_standard_time.hour)

    if minotaur_standard_time.minute[0] == "0":
        minotaur_minute = int(minotaur_standard_time.minute[1])
    else:
        minotaur_minute = int(minotaur_standard_time.minute)

    if minotaur_standard_time.second[0] == "0":
        minotaur_second = int(minotaur_standard_time.second[1])
    else:
        minotaur_second = int(minotaur_standard_time.second)

    if real_time.hour[0] == "0":
        real_hour = int(real_time.hour[1])
    else:
        real_hour = int(real_time.hour)

    if real_time.minute[0] == "0":
        real_minute = int(real_time.minute[1])
    else:
        real_minute = int(real_time.minute)

    if real_time.second[0] == "0":
        real_second = int(real_time.second[1])
    else:
        real_second = int(real_time.second)

    hour_diff = minotaur_hour - real_hour
    minute_diff = minotaur_minute - real_minute
    second_diff = minotaur_second - real_second
    total_diff = 3600*hour_diff + 60*minute_diff + second_diff
    direction = numpy.sign(total_diff)
    total_diff = math.fabs(total_diff)

    if total_diff == 0:
        THE_BEST = 1 / total_diff

    #print(minotaur_hour, minotaur_minute, minotaur_second)
    #print(real_hour, real_minute, real_second)
    #print(hour_diff, minute_diff, second_diff)

    if total_diff >= 120: # Need to make these different - instead of switch on or off based on difference, do something like LJ potential
        if direction == 1:
            minotaur_standard_time.state[2] = -1

        elif direction == -1:
            minotaur_standard_time.state[2] = 1

        minotaur_standard_time.state[3] = minotaur_standard_time.state[3]*random.uniform(1.0,4.0)
        return 0

    if 60 <= total_diff < 120:
        minotaur_standard_time.state[3] = minotaur_standard_time.state[3]*random.uniform(1.0,4.0)
        #change_chance = random.uniform(0.0,1.0)
        #if change_chance < 0.2:
        #    minotaur_standard_time.state[2] = numpy.sign(random.uniform(-1.0,1.0))
        return 1

    if 30 <= total_diff < 60:
        minotaur_standard_time.state[3] = minotaur_standard_time.state[3]*random.uniform(1.0,4.0)
        #change_chance = random.uniform(0.0,1.0)
        #if change_chance < 0.4:
        #    minotaur_standard_time.state[2] = numpy.sign(random.uniform(-1.0,1.0))
        return 2

        # do a more urgent thing
    if 10 <= total_diff < 30:
        minotaur_standard_time.state[3] = minotaur_standard_time.state[3]*random.uniform(0.3,1.0)
        #change_chance = random.uniform(0.0,1.0)
        #if change_chance < 0.6:
        #    minotaur_standard_time.state[2] = numpy.sign(random.uniform(-1.0,1.0))
        return 3

        # really urgent
    if 0 <= total_diff < 10:
        minotaur_standard_time.state[3] = minotaur_standard_time.state[3]*random.uniform(0.1,0.5)
        if direction == 1:
            minotaur_standard_time.state[2] = 1
        elif direction == -1:
            minotaur_standard_time.state[2] = -1
        return 4
        # run away


if __name__ == '__main__':

    global real_time, Dialog
    real_time = time_initializer()

    minotaur_standard_time = copy.copy(real_time) # MST initialization

    minotaur_standard_time.hour = real_time.hour # MST updating

    minotaur_standard_time.minute = (int(real_time.minute) - random.randrange(0,2)*int(numpy.sign(random.uniform(-1.0,1.0)))) % 60

    if minotaur_standard_time.minute < 10:
        minotaur_standard_time.minute = "0" + str(minotaur_standard_time.minute)
    else:
        minotaur_standard_time.minute = str(minotaur_standard_time.minute)

    minotaur_standard_time.second = random.randrange(0,59)
    if minotaur_standard_time.second < 10:
        minotaur_standard_time.second = "0" + str(minotaur_standard_time.second)
    else:
        minotaur_standard_time.second = str(minotaur_standard_time.second)

    minotaur_standard_time.state = [1, 1.0, 1, 3.0] # past direction, past speed, current direction, current speed


    app = QApplication(sys.argv)
    Dialog = QDialog()
    clock = BestClock()
    clock.setupUi()
    Dialog.show()

    sys.exit(app.exec_()) # Maybe make it jump around later!