import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import uic

WAIT, BUSY = range(2)

UI = '../UI/sma_th.ui'
GTR_STATUS = WAIT

# DRILL-REAMING
DRILL_STATUS = WAIT
TIME_DRILL = 20
LOAD_TIME_DRILL = 8
LOAD_TIME_STP1 = 8
LOAD_TIME_STP2 = 8
LOAD_TIME_SIDE = 8
TIME_CHECK = 2
UNCHECKED_NUM = 0
CHECKED_NUM = 0

# 4 STOPPER
STP1_STATUS = WAIT
STP1_A_STAT = 0
STP1_B_STAT = 0
TIME_STP = 35
LT_D_STP1 = 6
LT_S_STP1 = 6
LT_D_STP1_B = 12
LT_S_STP1_B = 12


class DrillMC(QThread):
    evtDrillProgress = QtCore.pyqtSignal(int)
    evtDrillComplete = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.isRun = False

    def run(self):
        global TIME_DRILL, DRILL_STATUS
        print('Drill Time:', TIME_DRILL)
        print('Drill Status:', DRILL_STATUS)
        while self.isRun:
            for i in range(TIME_DRILL):
                self.sleep(1)
                self.evtDrillProgress.emit(i+1)
                print('Drill time: ', i)

            self.evtDrillComplete.emit(8)
            DRILL_STATUS = WAIT
            print('Drill Status:', DRILL_STATUS)
            self.isRun = False


class Inspection(QThread):
    evtCheckComplete = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.isRun = False

    def run(self):
        global UNCHECKED_NUM, TIME_CHECK
        print('Check Time: ', TIME_CHECK)
        print('Unchecked:', UNCHECKED_NUM)
        while self.isRun:
            while UNCHECKED_NUM > 0:
                self.sleep(TIME_CHECK)
                UNCHECKED_NUM -= 1
                self.evtCheckComplete.emit(1)
                print('Check Complete: left ', UNCHECKED_NUM)

            self.isRun = False


class STP1(QThread):
    evtStp1AProgress = QtCore.pyqtSignal(int)
    evtStp1AComplete = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.isRun = False

    def run(self):
        global TIME_STP, STP1_STATUS
        print('STP1 Time:', TIME_STP)
        print('STP1 Status:', STP1_STATUS)
        while self.isRun:
            for i in range(TIME_STP):
                self.sleep(1)
                self.evtStp1AProgress.emit(i+1)
                print('stp1 time: ', i)

            STP1_STATUS = WAIT
            self.evtStp1AComplete.emit(2)
            print('STP1 Status:', STP1_STATUS)
            self.isRun = False


class Robot(QThread):
    evtNextWork = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.isRun = False

    def run(self):
        global GTR_STATUS, LOAD_TIME_DRILL, DRILL_STATUS, CHECKED_NUM
        global STP1_STATUS, LT_D_STP1, STP1_A_STAT, STP1_B_STAT, LT_D_STP1_B

        print('Robot instance called')
        while self.isRun:
            if GTR_STATUS == WAIT:
                if DRILL_STATUS == WAIT:
                    GTR_STATUS = BUSY
                    print('drill mc loading time: ', LOAD_TIME_DRILL)
                    time.sleep(LOAD_TIME_DRILL)
                    DRILL_STATUS = BUSY
                    self.evtNextWork.emit(0)
                    GTR_STATUS = WAIT
                elif CHECKED_NUM >= 6:
                    if STP1_STATUS == WAIT and not STP1_A_STAT and not STP1_B_STAT:
                        GTR_STATUS = BUSY
                        print('current checked work: ', CHECKED_NUM)
                        print('stp1 empty loading time: ', LT_D_STP1)
                        time.sleep(LT_D_STP1)
                        STP1_A_STAT = 3
                        STP1_STATUS = BUSY
                        self.evtNextWork.emit(1)
                        GTR_STATUS = WAIT
                    elif STP1_STATUS == WAIT and STP1_A_STAT == 2:
                        GTR_STATUS = BUSY
                        print('current checked work: ', CHECKED_NUM)
                        print('stp1 change loading time: ', LT_D_STP1_B)
                        time.sleep(LT_D_STP1_B)
                        STP1_A_STAT = 3
                        STP1_STATUS = BUSY
                        self.evtNextWork.emit(1)
                        GTR_STATUS = WAIT
            else:
                time.sleep(0.5)


class Dn8Sim(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI, self)
        self.setGeometry(100, 100, 640, 480)

        # 컨트롤 호출
        self.pbStart.clicked.connect(self.process)
        self.pbStop.clicked.connect(self.thread_stop)

        # 쓰레드 인스턴스 생성
        self.th_main = Robot(self)
        self.th_drill = DrillMC(self)
        self.th_check = Inspection(self)
        self.th_stp1 = STP1(self)

        # 쓰레드 이벤트 연결
        self.th_main.evtNextWork.connect(self.evtHandler_NextWork)
        self.th_drill.evtDrillProgress.connect(self.evtHandler_DrillProgress)
        self.th_drill.evtDrillComplete.connect(self.evtHandler_DrillComplete)
        self.th_check.evtCheckComplete.connect(self.evtHandler_CheckComplete)
        self.th_stp1.evtStp1AProgress.connect(self.evtHandler_Stp1Progress)
        self.th_stp1.evtStp1AComplete.connect(self.evtHandler_Stp1Complete)

        self.show()

    @pyqtSlot()
    def process(self):
        print('MC Activated')
        global LOAD_TIME_DRILL, LOAD_TIME_STP1, LOAD_TIME_STP2, LOAD_TIME_SIDE
        LOAD_TIME_DRILL = int(self.le_DrillLoading.text())
        LOAD_TIME_STP1 = int(self.le_Stp1Loading.text())
        LOAD_TIME_STP2 = int(self.le_Stp2Loading.text())
        LOAD_TIME_SIDE = int(self.le_SideLoading.text())

        global LT_D_STP1, LT_S_STP1, LT_D_STP1_B, LT_S_STP1_B
        LT_D_STP1 = int(self.le_Drill_To_STP1.text())
        LT_S_STP1 = int(self.le_Side_To_STP1.text())
        LT_D_STP1_B = int(self.le_Drill_STP1_To_Buff.text())
        LT_S_STP1_B = int(self.le_Side_STP1_To_Buff.text())

        if not self.th_main.isRun:
            self.th_main.isRun = True
            self.th_main.start()

    @pyqtSlot()
    def thread_stop(self):
        if self.th_main.isRun:
            print('Main : 쓰레드 정지')
            self.th_main.isRun = False

        if self.th_drill.isRun:
            print('Drill MC : 쓰레드 정지')
            self.th_drill.isRun = False

        if self.th_check.isRun:
            print('Inspection : 쓰레드 정지')
            self.th_check.isRun = False

        if self.th_stp1.isRun:
            print('STP1 : 쓰레드 정지')
            self.th_stp1.isRun = False

    # 쓰레드 이벤트 핸들러
    # 장식자에 파라미터 자료형을 명시
    @pyqtSlot(int)
    def evtHandler_DrillProgress(self, n):
        self.pgbDrill.setValue(n)
        self.pgbDrill.repaint()

    @pyqtSlot(int)
    def evtHandler_DrillComplete(self, n):
        global UNCHECKED_NUM
        UNCHECKED_NUM += n
        self.lcdUncheckedNum.display(UNCHECKED_NUM)

        global TIME_CHECK

        check_time = int(self.le_CheckTime.text())
        print('main:check time:', check_time)
        TIME_CHECK = check_time

        print("Drill MC call")
        if not self.th_check.isRun:
            self.th_check.isRun = True
            self.th_check.start()

    @pyqtSlot(int)
    def evtHandler_CheckComplete(self, n):
        global UNCHECKED_NUM, CHECKED_NUM
        CHECKED_NUM += n
        self.lcdCheckedNum.display(CHECKED_NUM)
        self.lcdUncheckedNum.display(UNCHECKED_NUM)

    @pyqtSlot(int)
    def evtHandler_Stp1Progress(self, n):
        self.pgbSTP1_A.setValue(n)
        self.pgbSTP1_A.repaint()
        self.cmbSTP1A.setCurrentIndex(3)

    @pyqtSlot(int)
    def evtHandler_Stp1Complete(self, n):
        self.cmbSTP1A.setCurrentIndex(n)

    @pyqtSlot(int)
    def evtHandler_NextWork(self, n):
        global TIME_DRILL, TIME_STP, CHECKED_NUM
        print('Next Work: ', n)

        if n == 0:
            self.lbl_RecentJob.setText('Drill-Reaming')
            drill_time = int(self.le_DrillTime.text())
            print('drill time:', drill_time)
            self.pgbDrill.setMaximum(drill_time)
            TIME_DRILL = drill_time

            print("Drill MC call")
            if not self.th_drill.isRun:
                self.th_drill.isRun = True
                self.th_drill.start()
        elif n == 1:
            self.lbl_RecentJob.setText('4-STOPPER #1')
            stp_time = int(self.le_STP1Time.text())
            print('stp1 time:', stp_time)
            self.pgbSTP1_A.setMaximum(stp_time)
            TIME_STP = stp_time
            CHECKED_NUM -= 6
            self.lcdCheckedNum.display(CHECKED_NUM)

            print("STP1 MC call")
            if not self.th_stp1.isRun:
                self.th_stp1.isRun = True
                self.th_stp1.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = Dn8Sim()
    sim.show()
    sys.exit(app.exec_())
