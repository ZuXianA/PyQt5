import os
import sys
import math
import socket
import threading


def sendFileList(new_socket):
    root_path = r'./'
    # 列出指定路径的文件以及文件夹 
    file_list = os.listdir(path=root_path)
    # 找出文件，剔除文件夹
    files = [file for file in file_list if os.path.isfile(file)]

    # print('---当前服务器文件如下所示---')
    new_socket.send('\n---当前服务器文件如下所示---\n'.encode('utf-8'))

    # 获取所有文件的大小
    for file in files:
        fsizebytes = os.path.getsize(filename=file)
        fsizekb = fsizebytes / 1024
        sned_content = '{}--------{:.2f}kb'.format(file,fsizekb)
        # print(sned_content)
        new_socket.send(sned_content.encode('utf-8'))
        
    new_socket.send('\n如需下载文件，请回复完整文件名，否则视为退出'.encode('utf-8'))

def sendFile(new_s):
    # 5. 接受客户端发过来的文件名
    download_filename = new_s.recv(1024)
    download_filename = download_filename.decode('utf-8')

    if os.path.exists(download_filename):  # 判断文件是否存在

        new_s.send(b'upload')

        #输出文件字节数
        fsizebytes = os.path.getsize(download_filename)
        # 转化为兆单位
        # fsizemb = fsizebytes / 1024 / 1024
        fsizemb = fsizebytes / 1024
        file_info = '文件：%s 的大小为：%.3fKB' % (download_filename,fsizemb)
        new_s.send(file_info.encode('utf-8'))
        # print(file_info)

        # 接受客户是否需要下载
        print('---等待对方发送确认下载请求---')

        options = new_s.recv(1024)
        if options == b'download':
            print('------开始发送------')
        
            with open(file=download_filename,mode='rb') as f:
                # 计算总数据包数目
                packag_nums = math.ceil(fsizebytes/1024)

                # 当前传输的数据包数目
                cnum = 0
                while True:
                    file_data = f.read(1024)

                    if file_data:
                        new_s.send(file_data)
                        cnum += 1
                        jindu = cnum / packag_nums * 100
                        print("当前已下载：%.2f%%" % jindu)
                    else:
                        print('---请求的文件数据发送完成---')
                        break
        else:
            print('下载取消！')
    else:
        new_s.send('\n404 Not Found'.encode('utf-8'))
        print('文件不存在！')
    
    new_s.close()

def subServer(new_socket):
    sendFileList(new_socket=new_socket)

    while True:
        sendFile(new_s=new_socket)
        break



def main():
    # 创建套接字
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 本地ip和端口号
    local_addr=("",9081)    # 修改端口在此处
    # 绑定本地ip
    server_socket.bind(local_addr)
    server_socket.listen(128)
    print('---套接字已创建，监听模式开启---')

    while True:
        print('\n已经连接的会话在后台运行，不想结束程序，不用回复即可！')
        signal = input('是否需要开启等待连接？')

        if signal != '0':
            # 给客户端分配一个新的socket，获取客户端的ip地址
            new_socket, client_address = server_socket.accept()
            print('客户端 %s(%s) 已连接' % (client_address[0],client_address[1]))

            threading.Thread(target=subServer, args=(new_socket,),daemon=True).start()
        else:
            server_socket.close()
            sys.exit()

if __name__ == '__main__':
    main()
