import socket
import threading

import fileServer
import main
import inspect
import ctypes
import time


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
        time.sleep(1)
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
        time.sleep(10)
        stop_thread(self.thread_)
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


threadLock = threading.Lock()
t1 = start_honeypot_thread(1, "root", "1234", "10.3.6.9", "2222")


t1.start()
t2 = stop_honey(t1)

if t1.is_alive():
    t2.start()


t3 = start_honeypot_thread(2, "root", "1234", "10.3.6.9", "2223")
t3.start()
