import socket
import sys

# from PyQt5.QtGui import QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from  DBConnection import  Db
import thirdpage as sp

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOGIN")
        self.setGeometry(500, 300, 600, 500)
        oImage = QImage("bg1.jpg")
        sImage = oImage.scaled(900, 600)
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        self.l0 = QLabel("LOGIN", self)
        self.l0.move(260, 110)
        self.l0.setText('Login')
        self.l0.setFont(QFont("Times", 17, QFont.Bold))
        self.l0.setStyleSheet('QLabel {color: red;}')

        self.l1 = QLabel("User name", self)
        self.l1.move(135, 190)
        self.l1.setFont(QFont("Times", 10, QFont.Bold))
        self.l1.setStyleSheet('QLabel {color: white;}')

        self.l2 = QLineEdit("", self)
        self.l2.move(250, 190)

        self.l3 = QLabel("Password", self)
        self.l3.setFont(QFont("Times", 10, QFont.Bold))
        self.l3.move(135, 230)
        self.l3.setStyleSheet('QLabel {color: white;}')

        self.l4 = QLineEdit("", self)
        self.l4.move(250, 230)
        self.l4.setEchoMode(QLineEdit.Password)

        # self.l16 = QPushButton("Forgot password", self)
        # self.l16.setStyleSheet("QPushButton { background-color: white }"
        #                        "QPushButton:pressed { background-color: white }")
        # self.l16.move(240, 260)
        # self.l16.setFont(QFont("Arial", 7, QFont.ExtraLight))
        # self.l16.clicked.connect(self.forgt)

        self.l5 = QPushButton("LOGIN", self)
        self.l5.move(270, 290)
        self.l5.resize(120,35)
        self.l5.setStyleSheet('QPushButton {background-color: #A3C1DA; font-size:18px}')
        self.l5.clicked.connect(self.clickmethod1)
        self.l9 = QLabel("", self)

        self.show()

    def clickmethod1(self):
        try:
            print("mmm")
            self.uname=self.l2.text()
            self.passwd=self.l4.text()
            if self.l2.text()==None:
                self.l2.setValidator('*')

            print(self.uname,self.passwd)
            db=Db()
            self.qry=db.selectOne("select * from login where Uname='"+self.uname+"' and passwd='"+self.passwd+"' and type='admin'")
            print('nnnn',self.qry)
            if self.qry is not None:
                self.type=self.qry['lid']
                print(self.type)
                db.delete("delete from sys_addr where user_id='" + str(self.type) + "'")
                self.ip_addr = socket.gethostbyname(socket.gethostname())
                print(self.ip_addr)
                adr = "insert into sys_addr(user_id,ip_adr) values('" + str(self.type) + "','" + self.ip_addr + "')"
                db.insert(adr)

                self.mm=sp.Example(self.type)
                self.m=self.hide()
            else:
                print("mmmmmmmmmmmmmmm")
                w1 = QWidget()
                QMessageBox.information(w1, "Message", "Incorrect Username or password.......")
                w1.setWindowTitle('Message..')

        except Exception as ex:
            print(ex)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())