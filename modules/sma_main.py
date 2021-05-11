# -*- coding: utf-8 -*-

import sys, time, os
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

smaUI = '../UI/sma.ui'

SCALING = 10
CONV_NUM = 0
CHK_NUM = 0
CHECKED = 0

DR, SP1, SP2, BUFFER, SIDE = range(5)

# machine status
DR_ON = False
SP1_1_ON = False
SP1_2_ON = False
SP2_1_ON = False
SP2_2_ON = False
SIDE_1_ON = False
SIDE_2_ON = False
GANTRY = DR


class DrillReaming:
    def __init__(self):
        self.unchecked = 0

    def process(self, sec, checkbox):
        checkbox.toggle()
        checkbox.repaint()
        time.sleep(sec)
        self.unchecked += 8
        checkbox.toggle()
        checkbox.repaint()

        return True


class Main(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(smaUI, self)
        self.dr = DrillReaming()
        self.pb_Start.clicked.connect(self.start_drill_reaming)
        self.pb_Hello.clicked.connect(self.hello_world)

    def start_drill_reaming(self):
        sec = int(self.le_ProcTime.text()) / SCALING
        tick = int(self.le_CheckTime.text()) / SCALING
        print('proc: ', sec, 'tick: ', tick)
        curr_check = int(self.numChecked.text())

        print(sec)
        if self.dr.process(sec, self.cbOnProc):
            global CONV_NUM
            CONV_NUM = CONV_NUM + 8
            print('conveyor: ', CONV_NUM)
            # self.numConv.setText(str(CONV_NUM + 8))
            self.numConv.setText(str(CONV_NUM))
            self.numConv.repaint()

        while self.dr.unchecked > 0:
            time.sleep(tick)
            global CHECKED
            CHECKED += 1
            print('Checked: ', CHECKED)
            self.numChecked.setText(str(CHECKED))
            self.numChecked.repaint()
            self.dr.unchecked -= 1

    def hello_world(self):
        print("Hello, world")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()

