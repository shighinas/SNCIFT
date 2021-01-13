import sys

# from PyQt5.QtGui import QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction,QMainWindow
from PyQt5.QtGui import QIcon
import addusers as sp
import viewusers as fp
import deleteuser as du
import secondpage as sp1
from DBConnection import Db


class Example(QMainWindow):
    def __init__(self,type):
        super().__init__()
        self.lid1=type
        print('ccccccccccccccccccc',self.lid1)

        self.setGeometry(500, 300, 500, 500)
        self.setWindowTitle('Home')
        self.setWindowIcon(QIcon('web.png'))

        menubar = self.menuBar()
        viewMenu = menubar.addMenu('File')

        viewStatAct = QAction('User', self)
        viewStatAct.setStatusTip('Start Application')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.mm)
        viewMenu.addAction(viewStatAct)

        viewStatAct = QAction('REGISTER', self)
        viewStatAct.setStatusTip('Start Application')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.clickmethod1)
        viewMenu.addAction(viewStatAct)

        viewStatAct = QAction('REMOVE', self)
        viewStatAct.setStatusTip('Start Application')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.clickmethod2)
        viewMenu.addAction(viewStatAct)

        viewStatAct = QAction('LOGOUT', self)
        viewStatAct.setStatusTip('Exit')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.clickmethod3)
        viewMenu.addAction(viewStatAct)

        self.show()

    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def mm(self):
        self.hh = fp.Apps(self.lid1)
        self.mm = self.hide()
    def clickmethod(self):
        self.hh=fp.Apps(self.lid1)
        self.mm=self.hide()

    def clickmethod1(self):
        self.hh = sp.Apps(self.lid1)
        self.mm = self.hide()

    def clickmethod2(self):
        self.hh = du.Apps(self.lid1)
        self.mm = self.hide()

    def clickmethod3(self):
        print(self.lid1,'mmmmmmmmmmmmm')
        db=Db()
        res=db.delete("delete from sys_addr where user_id='"+str(self.lid1)+"' ")
        print("kkkkkkkkkkkkkkkkkkkk",res)
        self.obj = sp1.Example()
        self.obj.show()  # load 2nd page
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())