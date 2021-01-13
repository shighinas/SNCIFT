import sys

# from PyQt5.QtGui import QPushButton
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
import secondpage as sp
import userlogin as ul


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 300, 600, 500)
        self.setWindowTitle('MAIN HOME')
        self.setWindowIcon(QIcon('web.png'))
        oImage = QImage("bg1.jpg")
        sImage = oImage.scaled(900, 600)
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        self.button = QPushButton('Login as Admin',self)
        self.button.resize(200,40)
        self.button.setStyleSheet('QPushButton {background-color: #A3C1DA; font-size:22px}')
        self.button.clicked.connect(self.clickmethod)
        self.button.move(200, 190)

        self.button1 = QPushButton(' Login as User ', self)
        self.button1.resize(200,40)
        self.button1.setStyleSheet('QPushButton {background-color: #A3C1DA; font-size:22px}')
        self.button1.clicked.connect(self.clickmethod1)
        self.button1.move(200, 250)
        self.show()

    def clickmethod(self):
        self.hh=sp.Example()
        self.mm=self.hide()

    def clickmethod1(self):
        self.hh = ul.App()
        self.mm = self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())