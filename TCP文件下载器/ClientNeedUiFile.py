import sys
import time
import socket
import threading
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import QApplication, QWidget

class MyWin(QWidget):

    updated_textBrowser = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("./DownloadUI.ui")
        
        self.local_ip = self.ui.comboBox            # 本地ip下拉菜单
        self.local_port = self.ui.lineEdit_1        # 本地port输入框
        self.ip_input = self.ui.lineEdit_2          # 对方ip输入框
        self.port_input = self.ui.lineEdit_3        # 对方port输入框
        self.turnon_btn = self.ui.checkBox
        self.link_btn = self.ui.checkBox_2
        self.send_btn = self.ui.checkBox_3
        self.recv_btn = self.ui.checkBox_4
        self.textEdit = self.ui.textEdit            # 发送数据编辑区域
        self.textBrowser = self.ui.textBrowser      # 接收数据显示区域

        self.getLocalIpAndDis()     # 添加本地ip到下拉菜单以供选择

        self.turnon_btn.toggled.connect(self.turnon)      # 绑定信息
        self.link_btn.clicked.connect(self.link)      # 绑定信息
       
        self.send_btn.clicked.connect(self.send_msg)      # 绑定信息

        self.updated_textBrowser.connect(slot=self.updateText)


    def getLocalIpAndDis(self):     # 获取本地IP和port
        local_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        self.local_ip.addItem(local_ip)

    def turnon(self):  # 打开TCP
        try:
            if self.turnon_btn.isChecked():
                local_port = self.local_port.text()
                local_ip = self.local_ip.currentText()
                s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
                s.bind((local_ip,int(local_port)))
                self.link_btn.setEnabled(True)          # 打开tcp后，允许点击连接按钮
                self.link_btn.setCheckState(False)      # 设置连接按钮为尚未点击状态
                self.socket = s
                self.textBrowser.setText('------TCP已打开------')
                
            else:
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket.close()
                self.textBrowser.setText('---TCP已关闭---')
        except:
            sys.exit()
              
    def link(self):     # 连接服务器
        try:
            ip_input = self.ip_input.text()
            port_input = self.port_input.text()
            self.socket.connect((ip_input,int(port_input)))
            self.textBrowser.setText('---连接服务器(%s)成功---' % ip_input)
            self.link_btn.setEnabled(False)             # 点击连接按钮之后，不允许再次点击
            threading.Thread(target=self.recv_msg,args=(),daemon=True).start()
        except:
            sys.exit()


    def download(self):
        
        # 5. 接受文件大小信息
        file_info = self.socket.recv(1024)
        file_info = file_info.decode('utf-8')
        self.updated_textBrowser.emit(file_info)

        # 6.获取文件大小
        download_filename = file_info.split('：')[1].split(' ')[0]
        fsizemb = file_info.split('：')[2].split('MB')[0]
        fsizekb = float(fsizemb) * 1024
        

        self.updated_textBrowser.emit('输入 download 即可开始下载')
        time.sleep(6)
        self.updated_textBrowser.emit('clear')

        with open(file=download_filename,mode='wb') as f:  ## 把数据写入到文件里
        # 目前接收到的数据包数目
            cnum = 0
            while True:
                file_data = self.socket.recv(1024)

                if file_data:
                    f.write(file_data)
                    cnum += 1
                    jindu = cnum / fsizekb * 100
                    self.updated_textBrowser.emit("当前已下载：%.2f%%" % jindu)
                    
                else:
                    self.updated_textBrowser.emit('------文件下载完成------')
                    break

        self.socket.close()


    def recv_msg(self):
        # 子线程不能调用主线程的函数，例如修改gui显示
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
            

def main():
    app = QApplication(sys.argv)

    w = MyWin()
    # 展示窗口
    w.ui.show()

    app.exec()


if __name__ == '__main__':
    main()
