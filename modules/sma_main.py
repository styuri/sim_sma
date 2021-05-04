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
checked = 0


class DrillReaming:
    def __init__(self):
        self.unchecked = 0

    def process(self, sec):
        time.sleep(sec)
        self.unchecked += 8

        return True


class Main(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(smaUI, self)
        self.dr = DrillReaming()
        self.pb_Start.clicked.connect(self.start_drill_reaming)

    def start_drill_reaming(self):
        sec = int(self.le_ProcTime.text()) / SCALING
        tick = int(self.le_CheckTime.text()) / SCALING
        print('proc: ', sec, 'tick: ', tick)
        curr_check = int(self.numChecked.text())

        print(sec)
        if self.dr.process(sec):
            self.numConv.setText(str(CONV_NUM + 8))
            self.numConv.repaint()

        while self.dr.unchecked > 0:
            time.sleep(tick)
            curr_check += 1
            self.numChecked.setText(str(curr_check))
            self.numChecked.repaint()
            self.dr.unchecked -= 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()

