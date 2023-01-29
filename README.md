##  TCP文件下载器
使用TCP协议实现文件下载功能。只需要将服务器源程序放在所要发送文件的目录下，客户端便可以直接下载

该文件夹下包含4个文件 ClientNeedUiFile.py、ClientWithUi.py、DownloadUl.ui、MultithreadedTCPserver.py

ClientNeedUiFile.py 为TCP客户端代码，需要加载 DownloadUl.ui 才能正常使用，进度条显示部分未做优化，可能会出现错误

ClientWithUi.py 为TCP客户端代码且集成 UI 界面，可以直接运行，进度条显示做了部分优化，能实现基本功能

MultithreadedTCPserver.py 为TCP服务器代码，使用集成终端运行，没有 UI 界面
