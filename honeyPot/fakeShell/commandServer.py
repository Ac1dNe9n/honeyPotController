import socket
import threading
import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib
import fileServer
import main
import inspect
import ctypes
import time


class start_file_logeer_thread(threading.Thread):
    def run(self):
        server = fileServer.Server()
        server.link_one_client()


class start_honeypot_thread(threading.Thread):
    def __init__(self, threadID, usr, psw, ip_, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.psw = psw
        self.ip_ = ip_
        self.port = port
        self.usr = usr

    def run(self):
        with open("thread_control/" + "pts" + str(self.threadID), "w") as f:
            f.write("0")
        time.sleep(5)
        main.createServer("test_rsa.key", self.threadID, ("", int(self.port)), self.usr, self.psw, self.ip_)


class start_file_logeer_thread(threading.Thread):
    def run(self):
        server = fileServer.Server()
        server.link_one_client()


class stop_honey(threading.Thread):
    def __init__(self, thread_):
        threading.Thread.__init__(self)
        self.thread_ = thread_

    def run(self):
        threadLock.acquire()
        with open("thread_control/" + "pts" + str(self.thread_.threadID), "w") as f:
            f.write("1")
        print("stop")
        stop_thread(self.thread_)
        time.sleep(5)
        threadLock.release()


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def link_one_client(addr):
    # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
    serverSocket = socket.socket()
    # 绑定监听的ip地址和端口号
    serverSocket.bind(addr)
    # 开始等待
    serverSocket.listen(5)

    log = start_file_logeer_thread()
    log.start()

    honeypot_list = []
    while True:
        clientSocket, addr = serverSocket.accept()
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

        # time.sleep(0.3)
        # 接收到的加密消息
        en_recvData = clientSocket.recv(1024)
        recvData = f.decrypt(en_recvData).decode()

        models = recvData.split(";")
        model = models[0]

        if model == '1':
            thread = start_honeypot_thread(models[1], models[2], models[3], models[4], models[5])
            thread.start()
            print(thread.threadID)
            honeypot_list.append(thread)
        elif model == '2':
            print("in 2")
            id_ = models[1]
            for honeypot in honeypot_list:
                if honeypot.threadID == id_:
                    t = stop_honey(honeypot)
                    t.start()
        elif model == '3':
            print("in 3")
            id_ = models[1]
            for honeypot in honeypot_list:
                print(honeypot.threadID)
                if honeypot.threadID == id_:
                    print("reset")
                    m1 = honeypot.threadID
                    m2 = honeypot.usr
                    m3 = honeypot.psw
                    m4 = honeypot.ip_
                    m5 = honeypot.port

                    stop_t = stop_honey(honeypot)
                    t_ = start_honeypot_thread(m1, m2, m3, m4, m5)
                    stop_t.start()

                    t_.start()

        sendData = "OK"
        # 对消息进行加密
        en_sendData = f.encrypt(sendData.encode())
        clientSocket.send(en_sendData)


if __name__ == '__main__':
    threadLock = threading.Lock()
    link_one_client(('192.168.152.136', 8088))
