import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage,QPalette, QBrush, QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QApplication, QFileDialog, QMessageBox, QWidget
from PyQt5.uic.properties import QtCore

from DBConnection import Db
import cv2
import skimage
import math
import numpy as np
import userloginiris as s
import userhome as ss

from scipy.spatial import Delaunay
from getTerminationBifurcation import getTerminationBifurcation;
from removeSpuriousMinutiae import removeSpuriousMinutiae
import socket

class App(QWidget) :
    def __init__(self):
        super().__init__()
        QWidget.__init__(self)
        self.setGeometry(400,200,680,500)

        oImage = QImage("finger log.png")
        sImage = oImage.scaled(QSize(680,500))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.showui()

    def showui(self):
        self.setWindowTitle("LOGIN FINGER")
        self.setGeometry(400,200,680,500)

        self.l0=QLabel("LOGIN",self)
        self.l0.move(270, 100)
        self.l0.setText('Login')
        self.l0.setFont(QFont("Times", 17,QFont.Bold))
        self.l0.setStyleSheet('QLabel {color: #5e736f;}')

        self.l9 = QLabel("", self)
        self.l9.setGeometry(180, 100, 100, 420)

        self.l10 = QLabel("Fingerprint", self)
        self.l10.setFont(QFont("Times", 10, QFont.Bold))
        self.l10.move(100, 200)

        self.l11 = QLineEdit("", self)
        self.l11.move(210, 198)

        self.l12 = QPushButton("Browse ", self)
        self.l12.move(273, 237)
        self.l12.setStyleSheet('QPushButton {background-color: #A3C1DA; font-size:17px}')
        self.l12.clicked.connect(self.clk1)

        self.l13 = QLabel("", self)
        self.l13.move(424, 180)

        self.l5 = QPushButton("NEXT",self)
        self.l5.move(273,291)
        self.l5.setStyleSheet('QPushButton {background-color: #A3C1DA; font-size:18px}')
        self.l5.clicked.connect(self.clk)

        self.show()

    def clk3(self):
        print("qwert")
         # load 2nd page
        # self.obj= Apps()
        # self.obj.show()
        # self.close()


    def clk(self):
        try:

            print('llllllllllllll',socket.gethostbyname(socket.gethostname()))
            # QMessageBox.about(self, "Status", "The server canot understand")

            print("hmmmmmmmmmmmmmmmmmm")
            self.maxdi = 0
            self.maxti = 0
            self.maxai = 0
            # print(len(self.tri.simplices))
            tricount=len(self.tri.simplices)
            rescount = 0
            for i in range(len(self.tri.simplices)):
                singletri = self.tri.simplices[i]
                p1 = singletri[0]
                p2 = singletri[1]
                p3 = singletri[2]

                x_a = self.bifx[p1]
                y_a = self.bify[p1]

                x_b = self.bifx[p2]
                y_b = self.bify[p2]

                x_c = self.bifx[p3]
                y_c = self.bify[p3]

                d1 = math.sqrt((x_a - x_b) ** 2 + (y_a - y_b) ** 2)
                d2 = math.sqrt((x_c - x_a) ** 2 + (y_c - y_a) ** 2)
                d3 = math.sqrt((x_b - x_c) ** 2 + (y_b - y_c) ** 2)

                a1 = math.acos((d2 ** 2 + d1 ** 2 - d3 ** 2) / (2 * d2 * d1))
                a2 = math.acos((d3 ** 2 + d1 ** 2 - d2 ** 2) / (2 * d3 * d1))
                a3 = math.acos((d3 ** 2 + d2 ** 2 - d1 ** 2) / (2 * d3 * d2))

                self.alphaa = (a1 / 180) * 3.14
                self.alphab = (a2 / 180) * 3.14
                self.alphac = (a3 / 180) * 3.14
                # print(self.alphaa,'mmmmmmmmmmmmmmmmmmmmm')
                SS = "SELECT * FROM finger_image WHERE (angle1='"+str(self.alphaa)+"' and angle2='"+str(self.alphab)+"' and angle3='"+str(self.alphac)+"') or (angle1='"+str(self.alphac)+"' and angle2='"+str(self.alphaa)+"' and angle3='"+str(self.alphab)+"') or (angle1='"+str(self.alphab)+"' and angle2='"+str(self.alphac)+"' and angle3='"+str(self.alphaa)+"')"
                c = Db()
                res = c.selectOne(SS)
                print(res)
                if res is not None:
                    rescount=rescount+1
                    print("rescount",rescount)
                    print("hmmmmmpppppppppppppppppppppppp")
                    ls = res['user_id']

            if rescount > int(((tricount) * 80) / 100):
                # ls=res['user_id']
                print("user id....." + str(ls))
                c = Db()

                c.delete("delete from sys_addr where user_id='" + str(ls) + "'")
                self.ip_addr = socket.gethostbyname(socket.gethostname())
                adr = "insert into sys_addr(user_id,ip_adr) values ('" + str(ls) + "','" + self.ip_addr + "')"
                c.insert(adr)
                print(str(ls))

            # self.obj = ss.MainWindow1(str(ls))
            # self.obj.show()  # load 2nd page
            # self.close()  # close current page

            self.obj=s.App(str(ls))
            self.obj.show()        #load 2nd page
            self.close()     #close current page

        except Exception as ex:
            print('nnnnnnnnnnnnnnnnnnnnnnn',ex)
            # QMessageBox.about(self, "Status", "The server canot understand")

    def clk1(self):
        try:
            self.app = QFileDialog.getOpenFileName(self, "files", "", "images(*.png *.xpm *.jpeg *.jpg)")
            self.l11.setText(self.app[0])
            print("??????????????????????????????????????????????????????")
            print("path")
            print(self.app[0])
            with open(self.app[0], 'r') as file_header:
                if self.app[0] == "":
                    print("0")
                else:
                    self.pixmap = QPixmap(self.app[0])
                    bb = self.pixmap.scaled(100, 100)
                    # self.l13.move(370, 130)
                    self.l13.resize(100, 100)
                    self.l13.setPixmap(bb)
                    self.t = QImage(self.app[0])

                    img = cv2.imread(self.app[0], 0);
                    img = np.uint8(img > 128);

                    skel = skimage.morphology.skeletonize(img)
                    skel = np.uint8(skel) * 255;

                    mask = img * 255;
                    (minutiaeTerm, minutiaeBif) = getTerminationBifurcation(skel, mask);

                    minutiaeTerm = skimage.measure.label(minutiaeTerm, 8);
                    RP = skimage.measure.regionprops(minutiaeTerm)
                    minutiaeTerm = removeSpuriousMinutiae(RP, np.uint8(img), 10);

                    BifLabel = skimage.measure.label(minutiaeBif, 8);
                    TermLabel = skimage.measure.label(minutiaeTerm, 8);

                    minutiaeBif = minutiaeBif * 0;
                    minutiaeTerm = minutiaeTerm * 0;

                    (rows, cols) = skel.shape
                    DispImg = np.zeros((rows, cols, 3), np.uint8)
                    DispImg[:, :, 0] = skel;
                    DispImg[:, :, 1] = skel;
                    DispImg[:, :, 2] = skel;
                    self.bifx = []
                    self.bify = []
                    RP = skimage.measure.regionprops(BifLabel)
                    for i in RP:
                        (row, col) = np.int16(np.round(i['Centroid']))
                        self.bifx.append(row)
                        self.bify.append(col)
                        minutiaeBif[row, col] = 1;
                        (rr, cc) = skimage.draw.circle_perimeter(row, col, 3);
                        skimage.draw.set_color(DispImg, (rr, cc), (255, 0, 0));

                    RP = skimage.measure.regionprops(TermLabel)
                    for i in RP:
                        (row, col) = np.int16(np.round(i['Centroid']))
                        minutiaeTerm[row, col] = 1;
                        self.bifx.append(row)
                        self.bify.append(col)
                        (rr, cc) = skimage.draw.circle_perimeter(row, col, 3);
                        skimage.draw.set_color(DispImg, (rr, cc), (0, 0, 255));
                    try:
                        cv2.imwrite("this.jpg", DispImg)
                    except Exception as ex:
                        print(ex)
                    try:
                        self.points = np.ndarray(shape=(len(self.bify), 2), dtype=int);

                        for i in range(len(self.bify)):
                            self.points[i][0] = self.bifx[i]
                            self.points[i][1] = self.bify[i]

                        self.tri = Delaunay(self.points)

                        i = 0
                        for a in self.tri.simplices:
                            i = i + 1
                            # print(a)


                    except Exception as ex:
                        print(ex)

                    # cv2.waitKey(0)
                    QMessageBox.about(self, "Status", "FInger upload completed you can proceeed now")
            # t1 = QWidget()
            # QMessageBox.information(t1, "Message", "Please Choose Path from directory..............")


        except Exception as ex:
            print(ex)


    # def angleplot(self):
    #
    #     self.maxdi = 0
    #     self.maxti = 0
    #     self.maxai = 0
    #
    #     arrda = []
    #     arrdb = []
    #     arrdc = []
    #     arra1 = []
    #     arra2 = []
    #     arra3 = []
    #     arralphaa = []
    #     arralphab = []
    #     arralphac = []
    #
    #     # print(len(self.tri.simplices))
    #
    #     for i in range(len(self.tri.simplices)):
    #         singletri = self.tri.simplices[i]
    #         p1 = singletri[0]
    #         p2 = singletri[1]
    #         p3 = singletri[2]
    #
    #         x_a = self.bifx[p1]
    #         y_a = self.bify[p1]
    #
    #         x_b = self.bifx[p2]
    #         y_b = self.bify[p2]
    #
    #         x_c = self.bifx[p3]
    #         y_c = self.bify[p3]
    #
    #         d1 = math.sqrt((x_a - x_b) ** 2 + (y_a - y_b) ** 2)
    #         d2 = math.sqrt((x_c - x_a) ** 2 + (y_c - y_a) ** 2)
    #         d3 = math.sqrt((x_b - x_c) ** 2 + (y_b - y_c) ** 2)
    #
    #         a1 = math.acos((d2 ** 2 + d1 ** 2 - d3 ** 2) / (2 * d2 * d1))
    #         a2 = math.acos((d3 ** 2 + d1 ** 2 - d2 ** 2) / (2 * d3 * d1))
    #         a3 = math.acos((d3 ** 2 + d2 ** 2 - d1 ** 2) / (2 * d3 * d2))
    #
    #         self.alphaa = (a1 / 180) * 3.14
    #         self.alphab = (a2 / 180) * 3.14
    #         self.alphac = (a3 / 180) * 3.14

    def go(self):
        print("hi")

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = App()
     sys.exit(app.exec())