import socket
from KeyAgreement import keyAgreementServer
from control import recoverVictim,createPlayGround,destoryPlayGround

def recoverSSH(aesPipeOUT, args):
    print('recoverSSH')
    _, port = recoverVictim('ssh')
    aesPipeOUT(str(port))

def addPlayGround(aesPipeOUT, args):
    print('addPlayGround')
    id = args[0]
    ip_addr = createPlayGround('PlayGround.' + id)
    aesPipeOUT(ip_addr)

def delPlayGround(aesPipeOUT, args):
    print('delPlayGround')
    id = args[0]
    destoryPlayGround('PlayGround.' + id)
    aesPipeOUT('OK')

def rePlayGround(aesPipeOUT, args):
    print('rePlayGround')
    id = args[0]
    destoryPlayGround('PlayGround.' + id)
    ip_addr = createPlayGround('PlayGround.' + id)
    aesPipeOUT(ip_addr)

def default(aesPipeOUT, args):
    print('default')
    aesPipeOUT('default')

if __name__ == '__main__':
    print('server start')
    HOST='0.0.0.0'
    PORT=20003
    MAX_WAITING=1

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
        
        msg = aesPipeIN()
        choice = msg.split(';')[0] #  split
        args = msg.split(';')[1:] #  split
        switch = {
            '1': recoverSSH,
            '2': addPlayGround,
            '3': delPlayGround,
            '4': rePlayGround,
        }
        switch.get(choice, default)(aesPipeOUT, args) 
        conn.close()