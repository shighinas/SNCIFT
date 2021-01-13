import hashlib
import sys
import socket
import base64
import pyaes
from stegano import lsb
from DBConnection import Db
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon,QPixmap,QImage,QColor,qRgb, QPalette ,QBrush
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QApplication, QFileDialog, QTextEdit, QMessageBox, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic.properties import QtWidgets
import cv2
import math
import numpy as np
import skimage.morphology
import skimage
from scipy.spatial import Delaunay
from getTerminationBifurcation import getTerminationBifurcation;
from removeSpuriousMinutiae import removeSpuriousMinutiae

# import userlogin as s

rpth = "C:\\RISS\\works\\python_tests\\FINGER\\"

class MainWindow1(QMainWindow):
    def __init__(self,uid):
        super().__init__()

        QMainWindow.__init__(self)
        self.uid=uid
        self.setMinimumSize(1350, 800)
        self.setWindowTitle("PyQt")

        QWidget.__init__(self)
        self.setGeometry(0, 0, 1350, 800)

        oImage = QImage("bg.jpg")
        sImage = oImage.scaled(QSize(1350,800))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.table = QTableWidget(parent=self)
        self.table.setColumnCount(9)

        self.table.setFixedSize(600, 300)
        self.table.move(700, 45)

        self.table.setHorizontalHeaderLabels(['Alpha - A', 'Alpha - B','Alpha - C','D1','D2','D3','Theta - A','Theta - B','Theta - C'])

        self.table1 = QTableWidget(parent=self)
        self.table1.setColumnCount(2)
        self.table1.setRowCount(2)
        self.table1.setFixedSize(250, 600)
        self.table1.move(10,50)
        self.table1.setHorizontalHeaderLabels(['USER', 'IP ADDRESS'])
        self.table1.clicked.connect(self.func_test)

        self.l1 = QLabel("Choose finger", self)
        # self.l2.setGeometry(400,50,200, 30)
        self.l1.move(280, 50)
        self.l2 = QLineEdit(" ", self)
        self.l2.setGeometry(400,50,170, 30)
        self.l2.move(400, 50)
        self.l5 = QPushButton("Browse..", self)
        self.l5.move(580, 50)
        self.l5.clicked.connect(self.clk)

        self.l3 = QLabel("Choose cover image", self)
        self.l3.setGeometry(400,320,370,30)
        self.l3.move(280, 280)
        self.l4 = QLineEdit(" ", self)
        self.l4.setGeometry(400,320,170,30)
        self.l4.move(390,320)
        self.l10 = QPushButton("Browse..", self)
        self.l10.move(570, 320)
        self.l10.clicked.connect(self.clk2)

        self.l16 = QPushButton("Apply Stegano and Send", self)
        self.l16.setGeometry(420, 355, 200, 40)
        self.l16.clicked.connect(self.stegano)

        self.l6 = QLabel("Finger image", self)
        self.l6.move(300, 200)
        self.l7 = QLabel("Cover image", self)
        self.l7.move(300, 400)

        self.l17 = QLabel("hide image", self)
        self.l17.move(470,400)

        # self.l9 = QLabel("Feature set extraction", self)
        self.l9 = QLabel("Cancellable template", self)
        self.l9.setGeometry(280, 530, 500,20)
        self.l9.move(280,540)
        self.l14 = QLineEdit(" ", self)
        self.l14.setGeometry(380,500,250,30)
        self.l14.move(435, 540)
        #self.l5 = QPushButton("Next", self)
        #self.l5.move(800, 590)
        #self.l5.clicked.connect(self.next)
        self.l11 = QLabel("Maximum Distance", self)
        self.l11.setGeometry(100, 1000, 150, 50)
        self.l12 = QPushButton("Merge", self)
        self.l12.setGeometry(330, 580,200,40)
        self.l12.move(470,580)
        self.l12.clicked.connect(self.send)
        self.l15 = QLabel("skeleton", self)
        self.l15.move(480, 200)

        self.l18 =QLabel("Receiver's template", self)
        self.l18.setGeometry(280, 530, 500,20)
        self.l18.move(280,640)
        #self.l18.clicked.connect(self.decod)
        self.l19 = QLineEdit(" ", self)
        self.l19.setGeometry(385,620,250, 30)
        self.l19.move(435, 640)
        self.l20 = QPushButton("logout", self)
        self.l20.move(50,15)
        self.l20.clicked.connect(self.logout)
        self.l22 = QLabel("Message", self)
        self.l22.move(900, 530)
        self.l23 = QLineEdit(" ", self)
        self.l23.setGeometry(800, 570, 350, 120)
        self.l20 = QPushButton("send", self)
        self.l20.clicked.connect(self.sendmsg)
        self.l20.move(1160,655)

        self.l24 = QLabel("Inbox", self)
        self.l24.move(900, 370)
        self.l25 = QTextEdit(" ", self)
        self.l25.setGeometry(800, 400, 350, 120)


        self.l21 = QPushButton("Refresh", self)
        self.l21.move(160,15)
        self.l21.clicked.connect(self.refresh)

        mythreadobj = mythread()
        mythreadobj.signal.connect(self.finished)
        mythreadobj.start()

        self.mythreadobj11 = receiverthread()
        self.mythreadobj11.signal.connect(self.finished1)
        self.mythreadobj11.start()
        #
        #
        #
        # mythreadobj.run()
        self.next()
        self.show()



    def refresh(self):
        print("===========")
        a = Db()
        s = "select Uid,ip_adr from user join sys_addr on user.Uid=sys_addr.user_id where sys_addr.user_id!='"+self.uid+"' "
        r = a.select(s)

        self.table1.setRowCount(len(r))
        self.table1.setColumnCount(2)

        for i in range(len(r)):
            self.table1.setItem(i, 0, QTableWidgetItem(str(r[i]["Uid"])))
            self.table1.setItem(i, 1, QTableWidgetItem(str(r[i]["ip_adr"])))

    def func_test(self, item):
        # http://www.python-forum.org/viewtopic.php?f=11&t=16817
        cellContent = item.data()
        print(cellContent)  # test
        self.rcvrip=format(cellContent)

    def rcvmsg(self):

        msg=self.l23.text()








    def next(self):
        a = Db()
        s ="select Uid,ip_adr from user join sys_addr on user.Uid=sys_addr.user_id where user.Uid!='"+str(self.uid)+"'"
        r = a.select(s)
        print(r)

        self.table1.setRowCount(len(r))
        self.table1.setColumnCount(2)

        for i in range(len(r)):
            self.table1.setItem(i, 0, QTableWidgetItem(str(r[i]['Uid'])))
            self.table1.setItem(i, 1, QTableWidgetItem(str(r[i]['ip_adr'])))


    def clk(self):

        self.app1 = QFileDialog.getOpenFileName(self, "files", "", "images(*.png *.xpm *.jpeg *.jpg )")
        self.l2.setText(self.app1[0])
        with open(self.app1[0], 'r') as file_header:
            if self.app1[0] == "":
                print("0")
            else:
                self.pixmap = QPixmap(self.app1[0])
                aa = self.pixmap.scaled(150, 150)
                self.l6.move(290, 130)
                self.l6.resize(120, 120)
                self.l6.setPixmap(aa)
                self.q = QImage(self.app1[0])

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
                    self.angleplot()
                except Exception as ex:
                    print(ex)
                # cv2.imshow('a',DispImg);
                self.pixmap1 = QPixmap("this.jpg")
                hh = self.pixmap1.scaled(400, 200)
                self.l15.move(465, 130)
                self.l15.resize(120, 120)
                self.l15.setPixmap(hh)
                self.q = QImage("this.jpg")
                cv2.waitKey(0)

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
        self.table.setRowCount(len(self.tri.simplices))
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

            alphaa = (a1 / 180) * 3.14
            alphab = (a2 / 180) * 3.14
            alphac = (a3 / 180) * 3.14

            da = (d1+d3)/2
            db= (d1+d2)/2
            dc= (d2+d3)/2

            arrda.append(da)
            arrdb.append(db)
            arrdc.append(dc)
            arra1.append(a1)
            arra2.append(a2)
            arra3.append(a3)
            arralphaa.append(alphaa)
            arralphab.append(alphab)
            arralphac.append(alphac)

            self.maxdi=max(self.maxdi,da,db,dc)
            self.maxai=max(self.maxai,alphaa,alphab,alphac)
            self.maxti=max(self.maxti,a1,a2,a3)

            aa = (abs(a1-a2)+abs(a1-a3))/2
            ab= (abs(a2-a1)+abs(a2-a3))/2
            ac= (abs(a3-a1)+abs(a3-a2))/2

            self.table.setItem(i, 0, QTableWidgetItem(str(alphaa)))
            self.table.setItem(i, 1, QTableWidgetItem(str(alphab)))
            self.table.setItem(i, 2, QTableWidgetItem(str(alphac)))
            self.table.setItem(i, 3, QTableWidgetItem(str(da)))
            self.table.setItem(i, 4, QTableWidgetItem(str(db)))
            self.table.setItem(i, 5, QTableWidgetItem(str(dc)))
            self.table.setItem(i, 6, QTableWidgetItem(str(aa)))
            self.table.setItem(i, 7, QTableWidgetItem(str(ab)))
            self.table.setItem(i, 8, QTableWidgetItem(str(ac)))

        self.l11.setText(str(self.maxdi))

        self.cx=float(self.maxdi/10)
        self.cy=float((self.maxai)/10)
        self.cz=float(self.maxti/10)

        print(self.cx,self.cy,self.cz)

        x=[0,0,0,0,0,0,0,0,0,0]
        y=[0,0,0,0,0,0,0,0,0,0]
        z=[0,0,0,0,0,0,0,0,0,0]

        threedim= np.zeros((10, 10, 10))

        for i in range(len(arrda)):
            # print("hi")
            arrda[i] = min(9,int(arrda[i]/self.cx))
            arra1[i] = min(9, int(arra1[i] / self.cy))
            arralphaa[i] = min(9, int(arralphaa[i] / self.cz))
            threedim[ arrda[i],arra1[i],arralphaa[i]]=1

            # print(arrda[i]/self.cx)
            arrdb[i] = min(9,int(arrdb[i]/self.cx))
            arra2[i] = min(9, int(arra2[i] / self.cy))
            arralphab[i] = min(9, int(arralphab[i] / self.cz))
            threedim[arrdb[i], arra2[i], arralphab[i]] = 1

            # print(arrdb[i]/self.cx)
            arrdc[i] = min(9,int(arrdc[i]/self.cx))
            arra3[i] = min(9,int(arra3[i]/self.cy))
            arralphac[i] = min(9,int(arralphac[i]/self.cz))
            threedim[arrdc[i], arra3[i], arralphac[i]] = 1

        # print("finished creating matrix")
        # print(x)
        # print(y)
        # print(z)

        # print(threedim)
        # print(threedim)
        cnc=""
        for i in threedim:
            for j in i :
                for k in j :
                    cnc=cnc+str(int(k))
        self.cnc=cnc
        self.l14.setText(str(cnc))
        # print(len(cnc))

    def sendmsg(self):
        a=self.l23.text()
        # a="ayyyyo ammme"
        import pyaes
        # self.mh="dsfds87y676"
        i =a
        if len(self.mh)>32:
            self.mh=self.mh[:32]

        key = self.mh + (32-len(self.mh)) *"0"
        print(key)
        aes = pyaes.AESModeOfOperationCTR(str.encode(key))
        e = aes.encrypt(i)
        a=e

        input=a
        print("encr",a)
        print(e)
        a=e
        msg=""
        if len(a)>0:
            print("haiiiiii")
            self.msg="entammmmmojjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj"
            # self.msg=self.messagetosedn.text()
            print(self.msg)
            Server_address1 = self.rcvrip
            Application_port1 = 3333
            print("Trying to sent packet")
            sok1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sok1.connect((Server_address1, Application_port1))
            print("connected to server")
            input = a
            # Whatever Is your buffer size
            splitLen = 5

            for lines in range(0, len(input), splitLen):
                outputData = input[lines:lines + splitLen]
                print("aaaa",outputData)
                sok1.send(outputData)
                print("sent packets")
            # sok1.send(EOF)
            sok1.close()
            print("Message sent successfully")
        else:
            msg = "Nothing to send"
            print(msg)
            QMessageBox.about(self,"Warning",msg)

        message=self.l23.text()
        # ms=self.l25.text()

        ms="\n" +"Me:"+message

        self.l25.append(ms)
        print(message)


    def send(self):
        mm=str(self.l14.text()).replace(" ","")
        ms=str(self.l19.text()).replace(" ","")
        print(mm,'kkkkkkkkkkkkkkkkkk')
        print(ms,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        s=""
        if len(mm) == len(ms):
            for i in range(0,len(mm)):
                a = int(mm[i])
                b = int(ms[i])
                print(a,b)
                xoring = a ^ b
                print(xoring)
                s = s + str(xoring)
            #     print(s)
            print(s)
            result = hashlib.sha1(s.encode('ascii'))


            print("The hexadecimal equivalent of SHA1 is : ")
            self.mh=str(result.hexdigest())
            QMessageBox.about(self,"Created  key."," Key="+self.mh)

    #def receive(self):
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_address = ('localhost', 10000
        #print(sys.stderr, 'starting up on %s port %s' % server_address)
        #sock.bind(server_address)
        #sock.listen(1)
        #while True:
            # Wait for a connection
            #print(sys.stderr, 'waiting for a connection')
            #connection, client_address = sock.accept()
            #try:
                #print(sys.stderr, 'connection from', client_address)

                # Receive the data in small chunks and retransmit it
               # while True:
                    #data = connection.recv(16)
                    #print(sys.stderr, 'received "%s"' % data)

                    # if data:
                    #     print(sys.stderr, 'sending data back to the client')
                    #     connection.sendall(data)
                    # else:
                    #     print(sys.stderr, 'no more data from', client_address)
                    #     break

            #finally:
                # Clean up the connection
                #connection.close()

    def clk2(self):

        self.app2 = QFileDialog.getOpenFileName(self, "files", "", "images(*.png *.xpm *.jpeg *.jpg)")
        self.l4.setText(self.app2[0])
        print("??????????????????????????????????????????????????????")
        print("path")
        print(self.app2[0])
        with open(self.app2[0], 'r') as file_header:

            if self.app2[0] == "":
                print("0")
            else:
                self.pixmap = QPixmap(self.app2[0])
                bb = self.pixmap.scaled(150, 150)
                # self.l7.move(285, 350)
                self.l7.resize(120, 120)
                self.l7.setPixmap(bb)
                self.t = QImage(self.app2[0])

    def stegano(self):
        try:
            a=Db()
            sd= "select userkey from key_table where user_id='"+str(self.uid)+"'"
            uid1=a.selectOne(sd)
            print(uid1)
            key="10928374635273849584736475876543"
            if uid1 is not None:
                key =str(uid1['userkey'])
                print("key",key)
                key = str(key) + (32 - len(key)) * 'h'
                print(key)
            plaintext = self.cnc
            key = key.encode('utf-8')
            aes = pyaes.AESModeOfOperationCTR(key)
            self.ciphertext = aes.encrypt(plaintext)
            print('nnnnn',plaintext)
            print("cipher",self.ciphertext)

            # key = key.encode('utf-8')
            aes = pyaes.AESModeOfOperationCTR(key)

            #print(ciphertext)
            # encrypted
            self.host_name = socket.gethostname()
            self.host_ip = socket.gethostbyname(self.host_name)
            print(self.host_ip)

            secret=lsb.hide(self.app2[0],str(plaintext)+"#"+self.host_ip)

            print("hii")
            secret.save("hidedimage1.png")

            self.pixmap2 = QPixmap("hidedimage1.png")
            kk = self.pixmap2.scaled(120, 120)
            # self.l17.move(450,350)
            self.l17.resize(120, 120)
            self.l17.setPixmap(kk)
            encoded_image_file =rpth+"hidedimage1.png"
            Server_address = str(self.rcvrip)
            Application_port = 2222
            print("Trying to sent packet")
            sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sok.connect((Server_address, Application_port))
            print("connected to server")
            with open(encoded_image_file, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            print(encoded_string)
            input = encoded_string
            splitLen = 20

            for lines in range(0, len(input), splitLen):
                outputData = input[lines:lines + splitLen]
                # print(outputData)
                sok.send(outputData)
            print("sending")

            # sok.send(EOF)
            sok.close()
            print("sending done")
        except Exception as ex:
            print(ex)
            print("error")

    def decod(self):
        try:
            clear_msg=lsb.reveal("my_file.png")
            print("helloo")
            aa=clear_msg.split("#")
            if len(aa) ==2:
                self.clear_msg=aa[0]
                self.rcvrip=aa[1]
                self.l19.setText(self.clear_msg)

                QMessageBox.about(self,"Alert","You recieved cancellable stegano image from "+self.rcvrip+" and its decoded")
            # a = conn()
            # sds = "select userkey from key_table where user_id='" + self.uid + "'"
            #
            # uid = a.selectone(sds)
            # key = str(uid[0])
            # key = key + (32 - len(key)) * 'h'
            #
            # key = key.encode('utf-8')
            # aes = pyaes.AESModeOfOperationCTR(key)
            #
            # decrypted = aes.decrypt(clear_msg).decode('utf-8')
            # print(decrypted)

            # print(decrypted == self.cnc)
            # s=""
        except Exception as ex:
            print(ex)

    def logout(self):
        try:
            a = Db()
            dele="delete from sys_addr where user_id='" + self.uid+ "'"
            print(dele)
            a.delete(dele)
            from userlogin import App as mj
            self.obj = mj()
            self.obj.show()  # load 2nd page
            self.hide()

        except Exception as ex:
            print(ex)

    def finished(self):
        print("file received successfully")
        self.decod()

    def finished1(self,a):
        # QMessageBox.about(self,"Message",a)
        #print("haiiii finished",a)
        # self.mh = "dsfds87y676"
        i = a

        if len(self.mh) > 32:
            self.mh= self.mh[:32]

        key = self.mh + (32 - len(self.mh)) * "0"
        print(key)
        aes = pyaes.AESModeOfOperationCTR(str.encode(key))
        print("kkkk",a,len(a))

        try:
            d = aes.decrypt(bytes(i))
            print("Decryped",d)
            ms = "\n" + "Other:" + d.decode("utf-8")
            self.l25.append(ms)
        except:
            print("errrr")

        # # or, use this directly
        # # d = pyaes.AESModeOfOperationCTR(str.encode(key)).decrypt(e)
        # self.ssrecievedmessage.setText(str(a))
        # print("Message Recieved Successfully")


from PyQt5.QtCore import QThread, pyqtSignal
import base64
import socket

class mythread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        print("hello1")
        a = ""

        # self.window.setText("haiiiiiii")

    def run(self):
        self.host_name = socket.gethostname()
        try:
            self.host_ip = socket.gethostbyname(self.host_name)
            print(self.host_ip)
            print("hello2")
            Server_address = self.host_ip
            print("starting listening on", Server_address,2222)
            Application_port = 2222
            serversoket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("hello3")
            serversoket.bind((Server_address, Application_port))
            print("hello4")
            serversoket.listen(1)
            print("server listening")

            (clientsoket, address) = serversoket.accept()
            print(address, "helllloooooooo addddreweeee")
            recieve = ""
            output = ""
            splitLen = 20
            c = 1
            indx = 0
            frame = bytearray(8 * 1024 * 1024)
            while (c != 0):
                recieve = clientsoket.recv(splitLen)
                c = len(recieve)
                # print(type(recieve))
                # print(len(recieve))
                # frame.append(recieve)
                # print(type(recieve))
                frame[indx:indx + len(recieve)] = recieve
                # print(recieve)
                indx = indx + len(recieve)
                # output=output+recieve
            # print(frame)

            newframe = bytes(indx)
            newframe = frame[0:indx]
            m = base64.b64decode(newframe)
            f = open('my_file.png', 'w+b')
            binary_format = bytearray(m)
            f.write(binary_format)
            f.close()

            print("Final output", "============================")
            clientsoket.close()
            self.signal.emit("Hellllo kk")
        except Exception as ex:
            print('vvvvvvvv',ex)

class receiverthread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    def __init__(self):
        QThread.__init__(self)
        a=""
    def run(self):
        import base64
        import socket
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        Server_address = self.host_ip
        print("start listening on",Server_address,3333)
        Application_port = 3333
        serversoket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversoket.bind((Server_address, Application_port))
        while(1):
            serversoket.listen(1)
            (clientsoket, address) = serversoket.accept()
            print("connected to  server side hloooi")
            recieve = ""
            output = ""
            splitLen = 5
            c = 1
            indx = 0
            frame = bytearray(1024 * 1024)
            while (c>0):
                recieve = clientsoket.recv(splitLen)

                print("-----------------------------")
                c = len(recieve)
                #print(len(c),"rr")
                # print(type(recieve))
                # print("lksssss", str(recieve))
                # output =  recieve
                # print(len(recieve))
                # frame=frame+output
                print(recieve)
                print("hello")
                frame[indx:indx + len(recieve)] = recieve

                # print(recieve)
                indx = indx + len(recieve)
            print(frame[:indx])
            print("reached")



                # frame[indx:indx + len(recieve)] = recieve
                # print(recieve)
                # indx = indx + len(recieve)
                # output=output+recieve

            #print("----------------------------------------------------------------", frame)
            frame=frame[:indx]
            clientsoket.close()
            self.signal.emit(frame)


class mythreadmessage(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        print("hello1")
        a = ""

        # self.window.setText("haiiiiiii")

    def run(self):
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        print(self.host_ip)
        print("hello2")
        Server_address = self.host_ip
        print("starting listening on", Server_address,4444)
        Application_port = 4444
        serversoket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("hello3")
        serversoket.bind((Server_address, Application_port))
        print("hello4")
        serversoket.listen(1)
        print("server listening")


        (clientsoket, address) = serversoket.accept()
        print(address, "hellllo addddreweeee")
        recieve = ""
        output = ""
        splitLen = 20
        c = 1
        indx = 0
        frame = bytearray(8 * 1024 * 1024)
        while (c != 0):
            recieve = clientsoket.recv(splitLen)
            c = len(recieve)
            # print(type(recieve))
            # print(len(recieve))
            # frame.append(recieve)
            # print(type(recieve))
            frame[indx:indx + len(recieve)] = recieve
            # print(recieve)
            indx = indx + len(recieve)


        print(frame[:indx],"hurrray")
            # output=output+recieve

        # print(frame)

        # newframe = bytes(indx)
        # newframe = frame[0:indx]
        # m = base64.b64decode(newframe)
        # f = open('my_file.png', 'w+b')
        # binary_format = bytearray(m)
        # f.write(binary_format)
        # f.close()

        # print("Final output", newframe)
        clientsoket.close()
        self.signal.emit("Hellllo")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow1(31)
    sys.exit(app.exec_())