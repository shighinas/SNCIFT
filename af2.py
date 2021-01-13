import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QImage, QBrush, QPalette

import  firstpage as pg



class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # self.setGeometry(150, 50, 500, 200)
        self.setWindowTitle("F.......I........")
        # self.setGeometry(65, 50, 600, 400)
        self.setGeometry(65, 50, 900, 600)
        # self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        # self.setStyleSheet("background-image: url(i2.jpg);")

        oImage = QImage("bg1.jpg")
        sImage = oImage.scaled(900, 600)
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)




        self.statusBar()

        self.home()

    def home(self):

        self.btn = QtGui.QPushButton("Start Application", self)
        self.btn.move(320, 430)
        self.btn.clicked.connect(self.download)
        self.btn.setStyleSheet("background-color:#D89B05;color:#3F03FB;font-size:20px;")
        self.btn.setFixedWidth(200)

        self.show()

    def download(self):
        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(50, 550, 800, 30)
        # self.progress.move(150, 250)

        self.progress.show()

        self.completed = 0


        while self.completed < 100:

            self.completed += 0.0001
            self.progress.setValue(self.completed)


        self.mms = self.hide()
        self.ex = pg.Example()



def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()