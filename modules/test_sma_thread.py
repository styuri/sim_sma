from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore  # QtCore를 명시적으로 보여주기 위해


class MyThread(QThread):
    # 쓰레드의 커스텀 이벤트
    # 데이터 전달 시 형을 명시해야 함
    threadEvent = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.isRun = False

    def run(self):
        while self.isRun:
            for i in range(8):
                print('가공완료 : ' + str(i))

                # 'threadEvent' 이벤트 발생
                # 파라미터 전달 가능(객체도 가능)
                self.threadEvent.emit(i)
                self.sleep(1)
            self.isRun = False


class Sim(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # GUI 컨트롤 생성 및 배치
        self.btn1 = QPushButton("1번", self)
        self.btn2 = QPushButton("2번", self)
        self.lbl1 = QLabel()
        self.lbl2 = QLabel()
        self.pgb1 = QProgressBar()

        # Layout 설정
        horiBox = QHBoxLayout()
        verBox1 = QVBoxLayout()
        verBox1.addWidget(self.btn1)
        verBox1.addWidget(self.btn2)
        verBox2 = QVBoxLayout()
        verBox2.addWidget(self.pgb1)
        verBox2.addWidget(self.lbl2)
        horiBox.addLayout(verBox1)
        horiBox.addLayout(verBox2)
        self.setLayout(horiBox)
        self.setGeometry(100, 100, 300, 100)

        # 컨트롤 호출
        self.btn1.clicked.connect(self.process)
        self.btn2.clicked.connect(self.hello)

        # 쓰레드 인스턴스 생성
        self.th = MyThread(self)
        # 쓰레드 이벤트 연결
        self.th.threadEvent.connect(self.threadEventHandler)

        self.show()

    def hello(self):
        print('Hello, world.')

    @pyqtSlot()
    def process(self):
        if not self.th.isRun:
            self.th.isRun = True
            self.th.start()

    # 쓰레드 이벤트 핸들러
    # 장식자에 파라미터 자료형을 명시
    @pyqtSlot(int)
    def threadEventHandler(self, n):
            self.lbl1.setText(str(n+1))
            self.lbl1.repaint()


if __name__ == '__main__':
    import sys, time

    app = QApplication(sys.argv)
    form = Sim()
    app.exec_()
