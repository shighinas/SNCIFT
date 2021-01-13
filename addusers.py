import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QFileDialog, \
    QMessageBox, QMainWindow, QAction
from PyQt5.QtGui import QIcon,QPixmap,QImage,QColor,qRgb,QPalette,QBrush,QFont
from DBConnection import Db
import random
import cv2
import skimage
import math
import numpy as np
import base64

from scipy.spatial import Delaunay
from getTerminationBifurcation import getTerminationBifurcation;
from removeSpuriousMinutiae import removeSpuriousMinutiae
import thirdpage as sp
import addusers as sp
import viewusers as fp
import deleteuser as du
import secondpage as sp1

from recognition import encode_photo

class Apps(QMainWindow) :
    def __init__(self,lid):
        super().__init__()
        self.lid1=lid
        QWidget.__init__(self)
        # self.setGeometry(500, 300, 800, 600)

        oImage = QImage("reg pic.png")
        sImage = oImage.scaled(QSize(650, 600))
        palette = QPalette()
        palette.setBrush(10,QBrush(sImage))
        self.setPalette(palette)


        self.showui()
        self.show()

    def showui(self):
        self.setWindowTitle("register_form")
        self.setGeometry(500, 300, 650, 600)

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

        self.l0=QLabel("SIGN UP",self)
        self.l0.setFont(QFont("Times", 12, QFont.Bold))
        self.l0.setStyleSheet('QLabel {color: #5e736f;}')
        self.l0.move(350,60)
        # ---------------------------------------------------
        self.l10 = QLabel("Finger Image", self)
        self.l10.move(100, 120)
        self.l10.setFont(QFont("Times", 9, QFont.Bold))

        self.l11 = QLineEdit("", self)
        self.l11.move(225, 120)
        self.l11.setFixedWidth(200)

        self.l12 = QPushButton("Browse ", self)
        self.l12.move(312, 160)
        self.l12.clicked.connect(self.clk2)

        self.l13 = QLabel("", self)
        self.l13.move(470, 100)

        # ...............................................

        self.l101 = QLabel("Iris Image", self)
        self.l101.move(100, 220)
        self.l101.setFont(QFont("Times", 9, QFont.Bold))

        self.l111 = QLineEdit("", self)
        self.l111.move(225, 220)
        self.l111.setFixedWidth(200)

        self.l121 = QPushButton("Browse ", self)
        self.l121.move(312, 260)
        self.l121.clicked.connect(self.clk6)

        self.l131 = QLabel("", self)
        self.l131.move(470, 210)

        # ..........................................

        self.l1 = QLabel("User name", self)
        self.l1.move(100, 320)
        self.l1.setFont(QFont("Times", 10, QFont.Bold))

        self.l2 = QLineEdit(" ", self)
        self.l2.move(225, 320)
        self.l2.setFixedWidth(200)

        # ..........................................

        self.l5 = QPushButton("REGISTER",self)
        self.l5.move(250,390)
        self.l5.resize(140,40)
        self.l5.setStyleSheet('QPushButton {background-color: #A3C1DA; font-size:21px}')
        self.l5.clicked.connect(self.clk1)

        self.l9 = QLabel("", self)
        self.l9.setGeometry(630, 600, 150, 30)
        # self.id1=0

    def clk3(self):
        print("qwert")
         # load 2nd page
        self.obj= sp.Example()
        self.obj.show()
        self.close()

    def clk1(self):
        print("hi")
        try:
            self.Uname=self.l2.text()
            self.Uname=self.Uname.strip()
            a=Db()
            self.conf=random.randint(0000,9999)

            ss=a.select("select * from login where Uname='"+self.Uname+"'")
            if ss is not None:
                b="insert into login(Uname,passwd) values('"+self.Uname+"','"+str(self.conf)+"')"
                self.id1=a.insert(b)

                s="insert into user(Uid,Uname) values('" + str(self.id1)+ "','"+self.Uname+"')"
                a.insert(s)

                self.keys=str(random.randint(00000000000000000000000000000000,99999999999999999999999999999999))
                bb = "insert into key_table(user_id,userkey) values('" + str(self.id1)+ "','" + str(self.keys)+ "')"
                a.insert(bb)

                QMessageBox.about(self, "Status", "              Success              ")

                self.l9.setText("OK")
                self.obj = Apps(self.lid1 )
                self.obj.show()  # load 2nd page
                self.hide()
            # self.close()
            else:
                QMessageBox.about(self, "Status", "Username Exists. Try with different Username")

        except Exception as ex:
            print(ex)
    def clk2(self):

        try:
            self.app1 = QFileDialog.getOpenFileName(self, "files", "", "images(*.png *.xpm *.jpeg *.jpg)")
            self.l11.setText(self.app1[0])
            print("??????????????????????????????????????????????????????")
            print("path")
            print(self.app1[0])
            with open(self.app1[0], 'r') as file_header:
                if self.app1[0] == "":
                    print("0")
                else:
                    self.pixmap = QPixmap(self.app1[0])
                    bb = self.pixmap.scaled(90, 90)
                    # self.l13.move(320, 95)
                    self.l13.resize(90, 90)
                    self.l13.setPixmap(bb)
                    self.t = QImage(self.app1[0])

                    img = cv2.imread(self.app1[0], 0);
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

                    self.angleplot()
                    cv2.waitKey(0)
        except Exception as ex:
            print(ex)

    def angleplot(self):

        self.maxdi=0
        self.maxti=0
        self.maxai=0

        arrda = []
        arrdb = []
        arrdc = []
        arra1 = []
        arra2 = []
        arra3 = []
        arralphaa = []
        arralphab = []
        arralphac = []

        #print(len(self.tri.simplices))
        a = Db()
        self.id2 = "select max(lid) as mx from login"
        id = a.selectOne(self.id2)
        v = id['mx']
        print(str(v))
        if v is None:
            v1 = 1
        else:
            v1 = v + 1
        qr="delete from finger_image where user_id='" + str(v1) + "'"
        a.delete(qr)

# ------------------------------------------------------------------------------------------

        print("hmmmmmmmmmmmmmmmmmm")

        # print(len(self.tri.simplices))
        tricount = len(self.tri.simplices)
        flg=0
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
            SS = "SELECT * FROM finger_image WHERE (angle1='" + str(self.alphaa) + "' and angle2='" + str(
                self.alphab) + "' and angle3='" + str(self.alphac) + "') or (angle1='" + str(
                self.alphac) + "' and angle2='" + str(self.alphaa) + "' and angle3='" + str(
                self.alphab) + "') or (angle1='" + str(self.alphab) + "' and angle2='" + str(
                self.alphac) + "' and angle3='" + str(self.alphaa) + "')"
            c = Db()
            res = c.selectOne(SS)
            print(res)
            if res is not None:
                rescount = rescount + 1
                print("rescount", rescount)
                print("hmmmmmpppppppppppppppppppppppp")
                ls = res['user_id']

        if rescount > int(((tricount) * 80) / 100):
            # ls=res['user_id']
            print("user id....." + str(ls))
            flg=1



# ------------------------------------------------------------------------------------------

        if flg==0 :

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

                ff = "insert into finger_image(user_id,angle1,angle2,angle3) values('" + str(v1) + "','" + str(self.alphaa) + "','" + str(self.alphab) + "','" + str(self.alphac) + "')"
                a.insert(ff)
            QMessageBox.about(self, "Status", "Finger upload completed. you can proceeed now")
        else:
            print("not ok")

    def clk6(self):
        try:
            self.app1 = QFileDialog.getOpenFileName(self, "files", "", "images(*.png *.xpm *.jpeg *.jpg)")
            self.l111.setText(self.app1[0])
            print("??????????????????????????????????????????????????????")
            print("path")
            fl=self.app1[0]

# ==========================================================================================
            img = cv2.imread(fl, 0)
            img = cv2.medianBlur(img, 5)
            cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, img.shape[0] / 64, param1=200, param2=30,
                                       minRadius=10, maxRadius=0)
            circles = np.uint16(np.around(circles))
            crop_img = None
            for i in circles[0, :]:
                # crop_img = cimg[i[1] - 3 * i[2]:i[1] + 3 * i[2] , i[0] - i[2] - 4 * i[2]:i[0] + 4 * i[2]]
                crop_img = cimg[i[1] - 3 * i[2]:i[1] + 3 * i[2], i[0] - 3 * i[2]:i[0] + 3 * i[2]]

            crop_img = cv2.resize(crop_img, (256, 256))
            if crop_img is not None:
                cv2.imwrite('sb.jpg', crop_img)
            else:
                cv2.imwrite('sb.jpg', cimg)
# ===========================================================================================
            self.pixmap = QPixmap(fl)
            bb = self.pixmap.scaled(90, 90)
            # self.l131.move(320, 230)
            self.l131.resize(90, 90)
            self.l131.setPixmap(bb)
# -------------------------------------------------------------------------------------------
            image = cv2.imread(fl)
            image = cv2.resize(image, (256, 256))

            print(image.shape)
            code, mask = encode_photo(image)

            a = Db()
            self.id2 = "select max(lid) as mx from login"
            id = a.selectOne(self.id2)
            v = id['mx']
            print(str(v))
            if v is None:
                v1 = 1
            else:
                v1 = v + 1

            qr = "delete from iris_image where uid='" + str(v1) + "'"
            a.delete(qr)
            print("------------------------------------------------------")

            np.savetxt("ircode.txt", code)
            z=None
            with open("ircode.txt", "rb") as imageFile:
                st = str(base64.b64encode(imageFile.read()))
                print(st)
                z = st[1:]
                print(z)

            np.savetxt("irmask.txt", mask)
            y = None
            with open("irmask.txt", "rb") as imageF:
                st = str(base64.b64encode(imageF.read()))
                print(st)
                y = st[1:]
                print(y)

            e = "insert into iris_image values('" + str(v1) + "'," + z + "," + y + ")"
            print(e)
            id1 = a.insert(e)

            QMessageBox.about(self, "Status", "Iris Image upload completed. you can proceeed now")

        except Exception as ex:
            print(ex)

    def angleplot(self):

        self.maxdi = 0
        self.maxti = 0
        self.maxai = 0

        arrda = []
        arrdb = []
        arrdc = []
        arra1 = []
        arra2 = []
        arra3 = []
        arralphaa = []
        arralphab = []
        arralphac = []

        # print(len(self.tri.simplices))
        a = Db()
        self.id2 = "select max(lid) as mx from login"
        id = a.selectOne(self.id2)
        v = id['mx']
        print(str(v))
        if v is None:
            v1 = 1
        else:
            v1 = v + 1
        qr = "delete from finger_image where user_id='" + str(v1) + "'"
        a.delete(qr)

        # ------------------------------------------------------------------------------------------
        print("hmmmmmmmmmmmmmmmmmm")
        # print(len(self.tri.simplices))
        tricount = len(self.tri.simplices)
        self.flg = 0
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
            SS = "SELECT * FROM finger_image WHERE (angle1='" + str(self.alphaa) + "' and angle2='" + str(
                self.alphab) + "' and angle3='" + str(self.alphac) + "') or (angle1='" + str(
                self.alphac) + "' and angle2='" + str(self.alphaa) + "' and angle3='" + str(
                self.alphab) + "') or (angle1='" + str(self.alphab) + "' and angle2='" + str(
                self.alphac) + "' and angle3='" + str(self.alphaa) + "')"
            c = Db()
            res = c.selectOne(SS)
            print(res)
            if res is not None:
                rescount = rescount + 1
                print("rescount", rescount)
                print("hmmmmmpppppppppppppppppppppppp")
                ls = res['user_id']

        if rescount > int(((tricount) * 80) / 100):
            # ls=res['user_id']
            print("user id....." + str(ls))
            self.flg = 1

    # ------------------------------------------------------------------------------------------
        if self.flg == 0 :
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

                ff = "insert into finger_image(user_id,angle1,angle2,angle3) values('" + str(v1) + "','" + str(
                    self.alphaa) + "','" + str(self.alphab) + "','" + str(self.alphac) + "')"
                a.insert(ff)

            QMessageBox.about(self, "Status", "Finger upload completed. you can proceeed now")
        else:
            print("user exists")
            QMessageBox.about(self, "Status", "User Exists.")


    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def mm(self):
        self.hh = fp.Apps(self.lid1)

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
    ex = Apps(1)
    sys.exit(app.exec_())
