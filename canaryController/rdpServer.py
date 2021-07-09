import json
import os
import socket
import struct
import requests


class RdpServer:
    def __init__(self, backlog=5, addr=('0.0.0.0', 7788)):
        # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
        self.serverSocket = socket.socket()
        # 绑定监听的ip地址和端口号
        self.serverSocket.bind(addr)
        # 开始等待
        self.serverSocket.listen(backlog)

    def link_one_client(self):
        os.chdir("file")
        while True:
            # 获取客户端对象和客户端地址
            clientSocket, addr = self.serverSocket.accept()
            # 打印
            print("建立连接\n目标主机地址为：{0}".format(addr))
            fhead = clientSocket.recv(struct.calcsize('128sI'))
            # print(fhead)
            if not fhead:
                continue
            filename, filesize = struct.unpack('128sI', fhead)
            print(filename.decode().strip('\00'))
            with open(filename.decode().strip('\00'), 'wb') as fl:
                ressize = filesize
                while True:
                    if ressize > 1024:
                        filedata = clientSocket.recv(1024)
                    else:
                        filedata = clientSocket.recv(ressize)
                    fl.write(filedata)
                    ressize -= len(filedata)
                    if ressize <= 0:
                        print("传输完成")
                        checkFile()
                        break


def checkFile():
    logs = readLog()
    if logs[0]['DisconnectTime'] != "Connecting..." and logs[0]['Success2Login'] == 'Yes':
        url = 'http://10.21.196.121/rdpHoneyPot/'
        fileTime = getFileName(logs[0]["ConnectTime"])
        fileName = ""
        temp = os.listdir()
        for i in temp:
            if i.find(fileTime):
                fileName = i
                break
        data = {'ip': logs[0]['ip'], 'port': logs[0]['port'], 'ConnectTime': logs[0]['ConnectTime'],
                "DisconnectTime": logs[0]['DisconnectTime'], 'fileName': fileName}
        requests.post(url, data)
    elif logs[0]['DisconnectTime'] != "Connecting...":
        url = 'http://10.21.196.121/rdpHoneyPot/'
        data = {'ip': logs[0]['ip'], 'port': logs[0]['port'], 'ConnectTime': logs[0]['ConnectTime'],
                "DisconnectTime": logs[0]['DisconnectTime']}
        requests.post(url, data)


def readLog():
    with open('file/log.txt', 'r+', encoding="utf8") as f:
        mydict = f.read()
        mydict = mydict.replace('{', ',{').replace(',', '', 1)
        mydict = '[' + mydict + ']'
        mydict = mydict.replace("'", '"')
        mydict = json.loads(mydict)
        return mydict[-1:]


def getFileName(ConnectTime):
    ConnectTime = ConnectTime.replace('-', '').replace(' ', '_').replace(':', '-')
    ConnectTime = ConnectTime.split(".")[0]
    return ConnectTime


if __name__ == '__main__':
    # server = RdpServer()
    # print("Start")
    # server.link_one_client()
    checkFile()
