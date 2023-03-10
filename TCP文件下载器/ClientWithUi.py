import sys
import math
import time
import socket
import threading
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QApplication, QWidget


class Ui_Form(QWidget):

    updated_textBrowser = QtCore.pyqtSignal(str)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 500)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(30, 70, 140, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(395, 70, 140, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(65, 40, 70, 15))
        self.label_1.setObjectName("label_1")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(545, 40, 72, 15))
        self.label_4.setObjectName("label_4")
        self.lineEdit_1 = QtWidgets.QLineEdit(Form)
        self.lineEdit_1.setGeometry(QtCore.QRect(180, 70, 70, 25))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(545, 70, 70, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(430, 40, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(180, 40, 72, 15))
        self.label_2.setObjectName("label_2")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(50, 180, 550, 300))
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(50, 120, 550, 51))
        self.textEdit.setObjectName("textEdit")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(268, 50, 55, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(Form)
        self.checkBox_2.setGeometry(QtCore.QRect(330, 50, 55, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(Form)
        self.checkBox_3.setGeometry(QtCore.QRect(268, 75, 55, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(Form)
        self.checkBox_4.setGeometry(QtCore.QRect(330, 75, 55, 20))
        self.checkBox_4.setObjectName("checkBox_4")

        self.local_ip = self.comboBox            # ??????ip????????????
        self.local_port = self.lineEdit_1        # ??????port?????????
        self.ip_input = self.lineEdit_2          # ??????ip?????????
        self.port_input = self.lineEdit_3        # ??????port?????????
        self.turnon_btn = self.checkBox     # ??????TCP??????
        self.link_btn = self.checkBox_2       # ?????????????????????
        self.send_btn = self.checkBox_3     # ??????????????????
        self.recv_btn = self.checkBox_4     # ????????????????????????
        self.textEdit = self.textEdit            # ????????????????????????
        self.textBrowser = self.textBrowser      # ????????????????????????

        self.getLocalIpAndDis()     # ????????????ip???????????????????????????

        self.turnon_btn.toggled.connect(self.turnon)      # ????????????
        self.link_btn.clicked.connect(self.link)      # ????????????
       
        self.send_btn.clicked.connect(self.send_msg)      # ????????????

        self.updated_textBrowser.connect(slot=self.updateText)    # ???????????????????????????????????????


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def getLocalIpAndDis(self):     # ????????????IP???port
        local_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        self.local_ip.addItem(local_ip)


    def turnon(self):  # ??????TCP
        try:
            if self.turnon_btn.isChecked():
                local_port = self.local_port.text()
                local_ip = self.local_ip.currentText()
                s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
                s.bind((local_ip,int(local_port)))
                self.link_btn.setEnabled(True)          # ??????tcp??????????????????????????????
                self.link_btn.setCheckState(False)      # ???????????????????????????????????????
                self.socket = s
                self.textBrowser.setText('------TCP?????????------')
            else:
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket.close()
                self.textBrowser.setText('---TCP?????????---')
        except:
            sys.exit()
    
    
    def link(self):     # ???????????????
        try:
            ip_input = self.ip_input.text()
            port_input = self.port_input.text()
            self.socket.connect((ip_input,int(port_input)))
            self.textBrowser.setText('---???????????????(%s)??????---' % ip_input)
            self.link_btn.setEnabled(False)             # ????????????????????????????????????????????????
            threading.Thread(target=self.recv_msg,args=(),daemon=True).start()
        except:
            sys.exit()


    def download(self):        
        # 5. ????????????????????????
        file_info = self.socket.recv(1024)
        file_info = file_info.decode('utf-8')
        self.updated_textBrowser.emit(file_info)

        # 6.??????????????????
        download_filename = file_info.split('???')[1].split(' ')[0]
        fsizemb = file_info.split('???')[2].split('KB')[0]
        fsizekb = math.ceil(float(fsizemb))                 # ????????????????????????????????????????????????
        
        self.updated_textBrowser.emit('?????? download ??????????????????')
        time.sleep(6)
        self.updated_textBrowser.emit('clear')

        with open(file=download_filename,mode='wb') as f:  ## ???????????????????????????
        # ?????????????????????????????????
            cnum = 0
            while True:
                file_data = self.socket.recv(1024)

                if file_data:
                    f.write(file_data)
                    cnum += 1
                    jindu = cnum / fsizekb * 100
                    self.updated_textBrowser.emit("??????????????????%.2f%%" % jindu)
                    
                else:
                    self.updated_textBrowser.emit('------??????????????????------')
                    break

        self.socket.close()


    def recv_msg(self):
        # ??????????????????????????????????????????????????????gui??????
        while True:
            recv_content = self.socket.recv(1024)
            if recv_content == b'upload':
                threading.Thread(target=self.download,args=()).start()
                return None
                
            elif len(recv_content) != 0:
                self.updated_textBrowser.emit(recv_content.decode('utf-8'))
            else:
                break
   

    def send_msg(self):
        s = self.textEdit.toPlainText()
        self.socket.send(s.encode('utf-8'))
        self.link_btn.setCheckState(False)
        self.send_btn.setCheckState(False)
    
        
    def updateText(self,msg):
        if msg != 'clear':
            self.textBrowser.append(msg)
        else:
            self.textBrowser.clear()

            
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "DownloadByTCP"))
        self.comboBox.setItemText(0, _translate("Form", "127.0.0.1"))
        self.lineEdit_2.setText(_translate("Form", "192.168.0.151"))
        self.label_1.setText(_translate("Form", "??????IP"))
        self.label_4.setText(_translate("Form", "??????Port"))
        self.lineEdit_1.setText(_translate("Form", "9080"))
        self.lineEdit_3.setText(_translate("Form", "9081"))
        self.label_3.setText(_translate("Form", "??????IP"))
        self.label_2.setText(_translate("Form", "??????Port"))
        self.checkBox.setText(_translate("Form", "??????"))
        self.checkBox_2.setText(_translate("Form", "??????"))
        self.checkBox_3.setText(_translate("Form", "??????"))
        self.checkBox_4.setText(_translate("Form", "??????"))

def main():
    app = QApplication(sys.argv)

    w = QtWidgets.QMainWindow()

    ui = Ui_Form()
    ui.setupUi(w)

    # ????????????
    w.show()

    app.exec()


if __name__ == '__main__':
    main()
