import sys
# from PyQt5.QtGui import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMainWindow, \
    QAction, QHeaderView
from PyQt5.QtGui import QIcon, QFont, QPalette, QBrush, QImage
from DBConnection import Db
import addusers as sp
import viewusers as fp
import deleteuser as du
import secondpage as sp1

class Apps(QMainWindow) :
    def __init__(self,lid):
        super().__init__()
        self.lid1 = lid
        print('ccccccccccccccccccc', self.lid1)
        QWidget.__init__(self)
        self.setGeometry(500, 300, 500, 500)

        oImage = QImage("reg pic.png")
        sImage = oImage.scaled(QSize(500,700))
        palette = QPalette()
        palette.setBrush(10,QBrush(sImage))
        self.setPalette(palette)
        self.showui()
        self.show()

    def showui(self):
        self.setWindowTitle("User")
        self.setGeometry(500, 300, 800, 600)

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

        self.l0=QLabel("USER",self)
        self.l0.setFont(QFont("Times", 18, QFont.Bold))
        self.l0.setStyleSheet('QLabel {color: #5e736f;}')
        self.l0.move(190,60)
        self.table1 = QTableWidget(parent=self)
        self.table1.setColumnCount(2)

        self.table1.horizontalHeader().setStretchLastSection(True)
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # self.table1.setRowCount(2)
        self.table1.setFixedSize(450, 450)
        self.table1.move(150, 50)
        self.table1.setHorizontalHeaderLabels(['USER ID', 'USER NAME'])
        self.table1.clicked.connect(self.func_test)
        self.next()

    def func_test(self, item):
            # http://www.python-forum.org/viewtopic.php?f=11&t=16817
            cellContent = item.data()
            print(cellContent)  # test
            self.rcvrip = format(cellContent)

    def next(self):
        a = Db()
        s ="select * from user "
        r = a.select(s)

        self.table1.setRowCount(len(r))
        self.table1.setColumnCount(2)

        for i in range(len(r)):
            self.table1.setItem(i, 0, QTableWidgetItem(str(r[i]['Uid'])))
            self.table1.setItem(i, 1, QTableWidgetItem(str(r[i]['Uname'])))

    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def mm(self):
        self.hh = fp.Apps(self.lid1 )


    def clickmethod(self):
        self.hh=fp.Apps(self.lid1 )
        self.mm=self.hide()

    def clickmethod1(self):
        self.hh = sp.Apps(self.lid1 )
        self.mm = self.hide()

    def clickmethod2(self):
        self.hh = du.Apps(self.lid1 )
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
    ex = Apps()
    sys.exit(app.exec_())