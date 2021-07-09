import os
import socket
import struct
import time
addr = ('192.168.46.164', 7788)

def send_log():
    # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
    clientSocket = socket.socket()
    # 连接服务器ip和7788端口
    clientSocket.connect(addr)
    file = 'log.txt'
    fhead = struct.pack('128sI', file.encode(), os.stat(file).st_size)
    # print(fhead)
    clientSocket.send(fhead)
    with open(file, 'rb') as fl:
        while True:
            filedata = fl.read(1024)
            if not filedata:
                break
            clientSocket.send(filedata)

def send_log_and_pyrpd_flie(time_in_name):
    # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
    clientSocket = socket.socket()
    # 连接服务器ip和7788端口
    clientSocket.connect(addr)

    # 传log ，此处代码冗余是必要的请勿优化（server端并非多线程）
    file = 'log.txt'
    fhead = struct.pack('128sI', file.encode(), os.stat(file).st_size)
    # print(fhead)
    clientSocket.send(fhead)
    with open(file, 'rb') as fl:
        while True:
            filedata = fl.read(1024)
            if not filedata:
                break
            clientSocket.send(filedata)
    clientSocket.close()
    
    
    clientSocket = socket.socket()
    # 连接服务器ip和7788端口
    clientSocket.connect(addr)
    # 传.pyrdp文件
    print("++++++++++++++++zhe NT lai chuan pyrdp wen jian le++++++++++++++++++++++")
    os.chdir("/home/root1/pyrdp/pyrdp_output/replays")
    files = os.listdir()
    for file in files:
        if file[11:28] == time_in_name:
            fhead = struct.pack('128sI', file.encode(), os.stat(file).st_size)
            clientSocket.send(fhead)
            print("+++++++++++zhe SB chuan le pyrdp wen jian tou le  ++++++++++++++++")
            with open(file, 'rb') as fl:
                while True:
                    filedata = fl.read(1024)
                    if not filedata:
                        break
                    print(len(filedata))
                    clientSocket.send(filedata)
        else:
            print("live")
    os.chdir("/home/root1/pyrdp")


def check_attack( time_in_name):
    print("++++++++++++++++++++++ta ta ma lai check le ++++++++++++++++")
    print("++++++++++++++++++++++"+time_in_name+"++++++++++++++++")
    flag = "No"
    os.chdir("/home/root1/pyrdp/pyrdp_output/replays")
    files = os.listdir()
    for file in files:
        print(file[11:28])
        if file[11:28] == time_in_name:
            flag = "Yes"
            print("+++++++++++++++++++hai ta ma check YES le ????+++++++++++++++++++++")
    os.chdir("/home/root1/pyrdp")
    
    return flag

