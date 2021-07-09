import socket
from home.KeyAgreement import keyAgreementClient


def sendSSHData(addr, mode, ip="", port="", id="", user="", pwd=""):
    if mode == '1':  # 添加蜜罐，需要id，user，psd
        data = mode + ";" + str(id) + ";" + user + ";" + pwd + ";" + ip + ";" + port
        sendMessage(addr, data)
    elif mode == '2':  # 删除蜜罐，id，
        data = mode + ";" + str(id)
        sendMessage(addr, data)
    elif mode == '3':  # 恢复蜜罐 id
        data = mode + ";" + str(id)
        sendMessage(addr, data)


def sendRealSSHData(addr, mode, potID=""):
    if mode == '1':  # 重启
        return sendMessage(addr, mode)
    elif mode == '2':  # 创建蜜罐，id，
        data = mode + ";" + str(potID)
        return sendMessage(addr, data)
    elif mode == '3':  # 删除
        data = mode + ";" + str(potID)
        return sendMessage(addr, data)
    elif mode == '4':
        data = mode + ";" + str(potID)
        return sendMessage(addr, data)


def sendMessage(addr, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    aesPipeIN, aesPipeOUT = keyAgreementClient(client)
    print("Connected to Server.")
    aesPipeOUT(message)
    retmsg = aesPipeIN()
    return retmsg
