import sys
import socket
import threading
from PyQt5.Qt import QApplication, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_UDP(QWidget):
    
    updated_textBrowser = QtCore.pyqtSignal(str)
    
    def __init__(self,UDP):
        super().__init__()
        self.setupUi(UDP)


    def setupUi(self, UDP):
        UDP.setObjectName("UDP")
        UDP.resize(661, 378)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"./res/ChatByUDP.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UDP.setWindowIcon(icon)
        UDP.setWindowOpacity(0.9)
        UDP.setStyleSheet("")
        self.label_1 = QtWidgets.QLabel(UDP)
        self.label_1.setGeometry(QtCore.QRect(75, 30, 70, 15))
        self.label_1.setObjectName("label_1")
        self.lineEdit_1 = QtWidgets.QLineEdit(UDP)
        self.lineEdit_1.setGeometry(QtCore.QRect(190, 60, 70, 25))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.label_2 = QtWidgets.QLabel(UDP)
        self.label_2.setGeometry(QtCore.QRect(190, 30, 72, 15))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(UDP)
        self.pushButton.setGeometry(QtCore.QRect(50, 110, 81, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(UDP)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 110, 81, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit = QtWidgets.QTextEdit(UDP)
        self.textEdit.setGeometry(QtCore.QRect(30, 170, 261, 111))
        self.textEdit.setObjectName("textEdit")
        self.comboBox = QtWidgets.QComboBox(UDP)
        self.comboBox.setGeometry(QtCore.QRect(40, 60, 140, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.label_4 = QtWidgets.QLabel(UDP)
        self.label_4.setGeometry(QtCore.QRect(470, 30, 72, 15))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(UDP)
        self.lineEdit_3.setGeometry(QtCore.QRect(470, 60, 70, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(UDP)
        self.label_3.setGeometry(QtCore.QRect(355, 30, 72, 15))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(UDP)
        self.lineEdit_2.setGeometry(QtCore.QRect(320, 60, 140, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(UDP)
        self.pushButton_3.setGeometry(QtCore.QRect(550, 40, 81, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.textBrowser_2 = QtWidgets.QTextBrowser(UDP)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 290, 621, 71))
        self.textBrowser_2.setStyleSheet("background=color:rgb(255, 255, 0)")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.line = QtWidgets.QFrame(UDP)
        self.line.setGeometry(QtCore.QRect(290, 20, 20, 261))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(UDP)
        self.line_2.setGeometry(QtCore.QRect(20, 10, 620, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(UDP)
        self.line_3.setGeometry(QtCore.QRect(630, 20, 20, 340))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(UDP)
        self.line_4.setGeometry(QtCore.QRect(10, 20, 20, 341))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.textBrowser = QtWidgets.QTextBrowser(UDP)
        self.textBrowser.setGeometry(QtCore.QRect(310, 100, 321, 181))
        self.textBrowser.setObjectName("textBrowser")
        self.line_5 = QtWidgets.QFrame(UDP)
        self.line_5.setGeometry(QtCore.QRect(20, 270, 620, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")

        '''???????????????????????????'''
        self.local_ip = self.comboBox            # ??????ip????????????
        self.local_port = self.lineEdit_1        # ??????port?????????
        self.ip_input = self.lineEdit_2          # ??????ip?????????
        self.port_input = self.lineEdit_3        # ??????port?????????
        self.blind_btn = self.pushButton         # ??????????????????
        self.send_btn = self.pushButton_2        # ??????????????????
        self.recv_btn = self.pushButton_3        # ???????????????????????????
        self.textEdit = self.textEdit            # ????????????????????????
        self.textBrowser = self.textBrowser      # ????????????????????????
        self.textBrowser2 = self.textBrowser_2   # ????????????????????????

        # ????????????????????????
        self.textEdit.setPlaceholderText('???????????????????????????????????????')
        self.textBrowser.setPlaceholderText('???????????????????????????')

        self.blind_btn.setFlat(False)   # ?????????????????????

        self.getLocalIpAndDis()     # ????????????ip???????????????????????????

        self.blind_btn.clicked.connect(self.blindInfo)                # ????????????
        self.send_btn.clicked.connect(self.sendMsg)                   # ????????????
        self.recv_btn.clicked.connect(self.textBrowser.clear)         # ????????????

        self.updated_textBrowser.connect(slot=self.updateText)        # ?????????????????????

        self.retranslateUi(UDP)
        QtCore.QMetaObject.connectSlotsByName(UDP)


    def getLocalIpAndDis(self):     # ??????????????????IP????????????????????????????????????
        local_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        self.local_ip.addItem(local_ip)


    def blindInfo(self):        # ????????????ip???port
        try:
            if not self.blind_btn.isFlat():
                local_port = self.local_port.text()
                local_ip = self.local_ip.currentText()
                s = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
                s.bind((local_ip,int(local_port)))
                self.socket = s
                self.blind_btn.setFlat(True)
                self.textBrowser.setText('---UDP??????????????????????????????---')
        
                rec = threading.Thread(target=self.recvMsg,args=(),daemon=True)
                rec.start()
            else:
                self.socket.close()
                self.blind_btn.setFlat(False)
                self.textBrowser.setText('------UDP?????????------')
        except:
                self.textBrowser.setText('?????????????????????????????????')


    def sendMsg(self):
        try:
            ip_input = self.ip_input.text()         # ??????ip??????????????????
            port_input = self.port_input.text()     # ??????port??????????????????
            s = self.textEdit.toPlainText()         # ????????????????????????????????????
            self.socket.sendto(s.encode('utf-8'),(ip_input,int(port_input)))    # ????????????
            self.textEdit.clear()
        except:
            self.textBrowser.setText('????????????????????????????????????????????????????????????????????????')


    def recvMsg(self):
        while True:
            try:
                recv_content,client_info = self.socket.recvfrom(1024)
                msg = '%s(%d):%s' % (client_info[0],client_info[1],recv_content.decode('utf-8'))
                self.updated_textBrowser.emit(msg)
            except:
                self.updated_textBrowser.emit('????????????????????????????????????UDP????????????')
                break


    def updateText(self,msg):
        self.textBrowser.append(msg)


    def retranslateUi(self, UDP):
        _translate = QtCore.QCoreApplication.translate
        UDP.setWindowTitle(_translate("UDP", "ChatByUDP"))
        self.label_1.setText(_translate("UDP", "??????IP"))
        self.lineEdit_1.setText(_translate("UDP", "9080"))
        self.label_2.setText(_translate("UDP", "??????Port"))
        self.pushButton.setText(_translate("UDP", "????????????"))
        self.pushButton_2.setText(_translate("UDP", "????????????"))
        self.textEdit.setHtml(_translate("UDP", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.comboBox.setItemText(0, _translate("UDP", "127.0.0.1"))
        self.label_4.setText(_translate("UDP", "??????Port"))
        self.lineEdit_3.setText(_translate("UDP", "9081"))
        self.label_3.setText(_translate("UDP", "??????IP"))
        self.lineEdit_2.setText(_translate("UDP", "192.168"))
        self.pushButton_3.setText(_translate("UDP", "????????????"))
        self.textBrowser_2.setHtml(_translate("UDP", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ff0000;\"> ?????????????????????????????????????????????????????????</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600; color:#ff0000;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ff0000;\"> ????????????????????????????????????????????????????????????????????????</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600; color:#ff0000;\"><br /></p></body></html>"))
        self.textBrowser.setHtml(_translate("UDP", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


def main():
    app = QApplication(sys.argv)

    w = QWidget()

    ui = Ui_UDP(w)

    # ????????????
    w.show()

    app.exec()


if __name__ == '__main__':
    main()
