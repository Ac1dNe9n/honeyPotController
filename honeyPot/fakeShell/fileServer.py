import operator
import os
import socket
import struct
import threading

import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib
import time


class Server:
    number = 0

    def __init__(self, backlog=5, addr=('192.168.152.136', 8081)):
        # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
        self.serverSocket = socket.socket()
        # 绑定监听的ip地址和端口号
        self.serverSocket.bind(addr)
        # 开始等待
        self.serverSocket.listen(backlog)

    # 该函数需要并行处理
    def link_one_client(self):
        # 获取客户端对象和客户端地址
        clientSocket, addr = self.serverSocket.accept()

        # 客户端数量加1
        Server.number = Server.number + 1
        # 标记当前客户端编号
        now_number = Server.number

        # 打印
        print("和客户端{0}建立连接\n目标主机地址为：{1}".format(now_number, addr))
        # 接受客户端传递的公钥
        # 这里可以加一个哈希函数检验公钥的正确性！
        # 运用pickle进行反序列化
        publicKeyPK, pubKeySha256 = pickle.loads(clientSocket.recv(1024))
        if hashlib.sha256(publicKeyPK).hexdigest() != pubKeySha256:
            print("error")
        else:
            publicKey = pickle.loads(publicKeyPK)
            print("已接受公钥")

        # 下面是用公钥加密对称密钥并传递的过程
        # 产生用于对称加密的密钥
        sym_key = Fernet.generate_key()
        # 用pickle进行序列化用来进行网络传输
        # 对密钥进行hash保证其准确性
        en_sym_key = rsa.encrypt(pickle.dumps(sym_key), publicKey)
        en_sym_key_sha256 = hashlib.sha256(en_sym_key).hexdigest()
        print("正在加密传送密钥")
        clientSocket.send(pickle.dumps((en_sym_key, en_sym_key_sha256)))

        # 这里可以添加密钥交换成功的函数

        # 初始化加密对象
        f = Fernet(sym_key)
        lennum = 0
        # 下面使用对称密钥进行加密对话的过程
        filelist = []

        while True:
            time.sleep(0.3)
            baseLog = os.path.dirname(__file__) + "/logfile/"
            print(baseLog)
            os.chdir(baseLog)

            files = os.listdir()
            for file in files:
                print(files)
                if not (file in filelist):
                    fhead = struct.pack('128sI', file.encode(), os.stat(file).st_size)
                    clientSocket.send(fhead)
                    with open(file, 'rb') as fl:
                        while True:
                            filedata = fl.read(1024)
                            if not filedata:
                                break
                            en_filedata = f.encrypt(filedata)
                            print(len(en_filedata))
                            clientSocket.send(en_filedata)
                else:
                    print("live")
            filelist = files


if __name__ == '__main__':
    server = Server()
    # while True:
    #     # 这里使用多线程可以避免服务器阻塞在一个客户端上
    #     t = threading.Thread(target=server.link_one_client)
    #     t.start()

    server.link_one_client()
