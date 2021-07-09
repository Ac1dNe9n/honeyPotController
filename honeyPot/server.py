import socket

from honeyPot.KeyAgreement import keyAgreementServer
from honeyPot.honeyPotServer import addWebDocker, delWebDocker, restartWebDockear, addMysqlDocker, delMysqlDocker, \
    restartMysqlDockear


def addWeb(aesPipeOUT, args):
    print('create')
    addWebDocker(args[0], args[1])
    aesPipeOUT('ok')


def delWeb(aesPipeOUT, args):
    print('del')
    delWebDocker(args[0])
    aesPipeOUT('ok')


def reWeb(aesPipeOUT, args):
    print('recovery')
    restartWebDockear(args[0])
    aesPipeOUT('ok')


def addMysql(aesPipeOUT, args):
    print('create')
    addMysqlDocker(args[0], args[1])
    aesPipeOUT('ok')


def delMysql(aesPipeOUT, args):
    print('del')
    delMysqlDocker(args[0])
    aesPipeOUT('ok')


def reMysql(aesPipeOUT, args):
    print('recovery')
    restartMysqlDockear(args[0])
    aesPipeOUT('ok')


def default(aesPipeOUT, args):
    print('default')
    aesPipeOUT('default')


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 20000
    MAX_WAITING = 1
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.listen(MAX_WAITING)
    server.setblocking(True)
    while True:
        conn, addr = server.accept()
        print(f'Connected with: {addr}')
        conn.setblocking(True)
        aesPipeIN, aesPipeOUT = keyAgreementServer(conn)
        message = aesPipeIN()
        choice = message.split(";")[0]
        args = message.split(";")[1:]
        switch = {
            '1': addWeb,
            '2': delWeb,
            '3': reWeb,
            '4': addMysql,
            '5': delMysql,
            '6': reMysql,
        }
        switch.get(choice, default)(aesPipeOUT, args)
        conn.close()
