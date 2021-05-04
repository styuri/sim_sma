from PySide2.QtWidgets import QApplication, QWidget, QPushButton


class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.setGeometry(50, 100, 800, 600)
        self.btn = QPushButton("Welcome to python class", self)
        self.btn.move(100, 100)
        self.btn.clicked.connect(self.prt_hello)

    def prt_hello(self):
        print(self.btn.text())


app = QApplication([])
form = Form()
form.show()
app.exec_()

