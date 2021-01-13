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
import userhome as uh
from recognition import encode_photo,compare_codes
import base64


from scipy.spatial import Delaunay
from getTerminationBifurcation import getTerminationBifurcation;
from removeSpuriousMinutiae import removeSpuriousMinutiae
import socket
class App(QWidget) :
    def __init__(self,m):
        super().__init__()
        QWidget.__init__(self)
        self.setGeometry(400,200,600,400)
        self.ld=m
        oImage = QImage("bm.jpeg")
        sImage = oImage.scaled(QSize(600,400))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.showui()

    def showui(self):
        self.setWindowTitle("LOGIN IRIS")
        self.setGeometry(400,200,600,400)

        self.l0=QLabel("LOGIN",self)
        self.l0.move(230, 50)
        self.l0.setText('Login')
        self.l0.setFont(QFont("Times", 17,QFont.Bold))
        self.l0.setStyleSheet('QLabel {color: white;}')


        self.l9 = QLabel("", self)
        self.l9.setGeometry(180, 100, 100, 420)

        self.l10 = QLabel("Iris", self)
        self.l10.setFont(QFont("Times", 10, QFont.Bold))
        self.l10.setStyleSheet('QLabel {color: white;}')
        self.l10.move(130, 120)

        self.l11 = QLineEdit("", self)
        self.l11.move(190, 120)
        self.l11.setFixedWidth(180)

        self.l12 = QPushButton("Browse ", self)
        self.l12.move(260, 160)
        self.l12.setStyleSheet('QPushButton {background-color: #A3C1DA; font-size:17px}')
        self.l12.clicked.connect(self.clk1)

        self.l13 = QLabel("", self)
        self.l13.move(400, 140)
        self.l13.setStyleSheet('QLabel {color: white;}')

        self.l5 = QPushButton("LOGIN",self)
        self.l5.move(220,250)
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
            pth=self.l11.text()
            print(pth)
            db = Db()
            # ===========================================================================================
            image = cv2.imread(pth)
            image = cv2.resize(image, (256, 256))
            print(image.shape)
            code1, mask1 = encode_photo(image)
            # -------------------------------------------------------------------------------------------
            s = db.selectOne("select * from iris_image where uid='"+self.ld+"'")
            x = s['iris_code']
            m = s['mask']

            st1 = bytes(x, encoding="UTF-8")
            zz = base64.b64decode(st1)
            fh = open("im1.txt", "wb")
            fh.write(zz)
            fh.close()
            y = np.loadtxt("im1.txt")
            print(y)

            st2 = bytes(m, encoding="UTF-8")
            zz2 = base64.b64decode(st2)
            fh2 = open("im2.txt", "wb")
            fh2.write(zz2)
            fh2.close()
            ym = np.loadtxt("im2.txt")
            print(ym)

            result=compare_codes(code1, y, mask1, ym)
            print(result)
            if result< 0.2 :
                QMessageBox.about(self, "Status", "          Login Success          ")
                self.obj = uh.MainWindow1(str(self.ld))
                self.obj.show()  # load 2nd page
                self.close()  # close current page
            else:
                QMessageBox.about(self, "Status", "       Unknown user        ")

            # -------------------------------------------------------------------------------------------
        except Exception as ex:
            print('nnnnnnnnnnnnnnnnnnnnnnn',ex)
            QMessageBox.about(self, "Status", "Incorrect File")


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
                    # self.pixmap = QPixmap(self.app[0])
                    # bb = self.pixmap.scaled(100, 100)
                    # # self.l13.move(370, 130)
                    # self.l13.resize(100, 100)
                    # self.l13.setPixmap(bb)
                    # self.t = QImage(self.app[0])

        # ===========================================================================

                    img = cv2.imread(self.app[0], 0)
                    img = cv2.medianBlur(img, 5)
                    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

                    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, img.shape[0] / 64, param1=200, param2=30,
                                               minRadius=10, maxRadius=0)
                    circles = np.uint16(np.around(circles))
                    crop_img = None
                    for i in circles[0, :]:
                        # draw the outer circle
                        # cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                        # draw the center of the circle
                        # cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

                        # immm=cv2.rectangle(cimg,(i[0]-i[2],i[1]-i[2]),(i[0]+i[2],i[1]++i[2]),(0,0,255),3)

                        x = 10
                        crop_img = cimg[i[1] - i[2] - x:i[1] + i[2] + x, i[0] - i[2] - x:i[0] + i[2] + x]
                        # cv2.imshow("cropped", crop_img)
                        # cv2.waitKey(0)

                    if crop_img is not None:
                        cv2.imwrite('sb.jpg', crop_img)
                        # cv2.waitKey(0)
                        self.pixmap = QPixmap('sb.jpg')
                        bb = self.pixmap.scaled(100, 100)
                        # self.l13.move(370, 130)
                        self.l13.resize(100, 100)
                        self.l13.setPixmap(bb)
                    else:
                        cv2.imwrite('ir.jpg', cimg)
                        # cv2.waitKey(0)
                        self.pixmap = QPixmap('ir.jpg')
                        bb = self.pixmap.scaled(100, 100)
                        # self.l13.move(370, 130)
                        self.l13.resize(100, 100)
                        self.l13.setPixmap(bb)










        #
        #             img = cv2.imread(self.app[0], 0);
        #             img = np.uint8(img > 128);
        #
        #             skel = skimage.morphology.skeletonize(img)
        #             skel = np.uint8(skel) * 255;
        #
        #             mask = img * 255;
        #             (minutiaeTerm, minutiaeBif) = getTerminationBifurcation(skel, mask);
        #
        #             minutiaeTerm = skimage.measure.label(minutiaeTerm, 8);
        #             RP = skimage.measure.regionprops(minutiaeTerm)
        #             minutiaeTerm = removeSpuriousMinutiae(RP, np.uint8(img), 10);
        #
        #             BifLabel = skimage.measure.label(minutiaeBif, 8);
        #             TermLabel = skimage.measure.label(minutiaeTerm, 8);
        #
        #             minutiaeBif = minutiaeBif * 0;
        #             minutiaeTerm = minutiaeTerm * 0;
        #
        #             (rows, cols) = skel.shape
        #             DispImg = np.zeros((rows, cols, 3), np.uint8)
        #             DispImg[:, :, 0] = skel;
        #             DispImg[:, :, 1] = skel;
        #             DispImg[:, :, 2] = skel;
        #             self.bifx = []
        #             self.bify = []
        #             RP = skimage.measure.regionprops(BifLabel)
        #             for i in RP:
        #                 (row, col) = np.int16(np.round(i['Centroid']))
        #                 self.bifx.append(row)
        #                 self.bify.append(col)
        #                 minutiaeBif[row, col] = 1;
        #                 (rr, cc) = skimage.draw.circle_perimeter(row, col, 3);
        #                 skimage.draw.set_color(DispImg, (rr, cc), (255, 0, 0));
        #
        #             RP = skimage.measure.regionprops(TermLabel)
        #             for i in RP:
        #                 (row, col) = np.int16(np.round(i['Centroid']))
        #                 minutiaeTerm[row, col] = 1;
        #                 self.bifx.append(row)
        #                 self.bify.append(col)
        #                 (rr, cc) = skimage.draw.circle_perimeter(row, col, 3);
        #                 skimage.draw.set_color(DispImg, (rr, cc), (0, 0, 255));
        #             try:
        #                 cv2.imwrite("this.jpg", DispImg)
        #             except Exception as ex:
        #                 print(ex)
        #             try:
        #                 self.points = np.ndarray(shape=(len(self.bify), 2), dtype=int);
        #
        #                 for i in range(len(self.bify)):
        #                     self.points[i][0] = self.bifx[i]
        #                     self.points[i][1] = self.bify[i]
        #
        #                 self.tri = Delaunay(self.points)
        #
        #                 i = 0
        #                 for a in self.tri.simplices:
        #                     i = i + 1
        #                     # print(a)
        #
        #
                    # except Exception as ex:
                    #     print(ex)
        #
        #             # cv2.waitKey(0)
                    QMessageBox.about(self, "Status", "Iris upload completed you can proceeed now")
        #     # t1 = QWidget()
        #     # QMessageBox.information(t1, "Message", "Please Choose Path from directory..............")
        #
        #
        except Exception as ex:
            print(ex)

        # QMessageBox.about(self, "Status", "Iris upload completed you can proceeed now")

    def go(self):
        print("hi")

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = App()
     sys.exit(app.exec())