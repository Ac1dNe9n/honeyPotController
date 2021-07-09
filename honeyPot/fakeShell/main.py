import base64
from binascii import hexlify
import socket
import sys
import threading
import traceback
import paramiko
from paramiko.py3compat import b, u, decodebytes
import time
import uuid
import command_dispatcher
import linuxCommand
import os
import logSender


def log(sentence, ip, fileName="command_log.txt"):
    localtime = time.asctime(time.localtime(time.time()))
    baseLog = os.path.dirname(__file__) + "/logfile/"
    fileLoc = baseLog + fileName
    f = open(fileLoc, "a+")
    if f.read():
        f.write("client_ip" + "\t" + "time" + "\t" + "command\n")
        f.close()
    with open(fileLoc, "a") as f:
        f.write(str(ip) + "\t" + localtime + "\t" + sentence + "\n")


def createServer(rsa_key_filename, thread_id, address=("", 2200), usr_="root", psw_="1234", ip_str="127.0.0.1"):
    class Server(paramiko.ServerInterface):
        data = (
            b"AAAAB3NzaC1yc2EAAAABIwAAAIEAyO4it3fHlmGZWJaGrfeHOVY7RWO3P9M7hp"
            b"fAu7jJ2d7eothvfeuoRFtJwhUmZDluRdFyhFY/hFAh76PJKGAusIqIQKlkJxMC"
            b"KDqIexkgHAfID/6mqvmnSJf0b5W8v5h2pI/stOSwTQ+pxVhwJ9ctYDhRSlF0iT"
            b"UWT10hcuO4Ks8="
        )
        good_pub_key = paramiko.RSAKey(data=decodebytes(data))

        def __init__(self, usr=usr_, psw=psw_):
            self.event = threading.Event()
            self.usr = usr
            self.psw = psw

        def check_channel_request(self, kind, chanid):
            if kind == "session":
                return paramiko.OPEN_SUCCEEDED
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def check_auth_password(self, username, password):
            if (username == self.usr) and (password == self.psw):
                return paramiko.AUTH_SUCCESSFUL
            return paramiko.AUTH_FAILED

        def check_auth_publickey(self, username, key):
            print("Auth attempt with key: " + u(hexlify(key.get_fingerprint())))
            if (username == self.usr) and (key == self.good_pub_key):
                return paramiko.AUTH_SUCCESSFUL
            return paramiko.AUTH_FAILED

        def check_auth_gssapi_with_mic(
                self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
        ):
            if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
                return paramiko.AUTH_SUCCESSFUL
            return paramiko.AUTH_FAILED

        def check_auth_gssapi_keyex(
                self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
        ):
            if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
                return paramiko.AUTH_SUCCESSFUL
            return paramiko.AUTH_FAILED

        def enable_auth_gssapi(self):
            return True

        def get_allowed_auths(self, username):
            return "gssapi-keyex,gssapi-with-mic,password,publickey"

        def check_channel_shell_request(self, channel):
            self.event.set()
            return True

        def check_channel_pty_request(
                self, channel, term, width, height, pixelwidth, pixelheight, modes
        ):
            return True

    host_key = paramiko.RSAKey(filename=rsa_key_filename)

    print("Read key: " + u(hexlify(host_key.get_fingerprint())))

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(address)
    except Exception as e:
        print("*** Bind failed: " + str(e))
        traceback.print_exc()
        sys.exit(1)

    try:
        sock.listen(100)
        print("Listening for connection ...")
        client, addr = sock.accept()
    except Exception as e:
        print("*** Listen/accept failed: " + str(e))
        traceback.print_exc()
        sys.exit(1)

    print("Got a connection!")
    try:
        t = paramiko.Transport(client)
        t.set_gss_host(socket.getfqdn(""))
        try:
            t.load_server_moduli()
        except:
            print("(Failed to load moduli -- gex will be unsupported.)")
            raise
        t.add_server_key(host_key)
        server = Server()
        try:
            t.start_server(server=server)
        except paramiko.SSHException:
            print("*** SSH negotiation failed.")
            sys.exit(1)

        # wait for auth
        chan = t.accept(200)
        if chan is None:
            print("*** No channel.")
            sys.exit(1)
        print("Authenticated!")

        server.event.wait(1)
        if not server.event.is_set():
            print("*** Client never asked for a shell.")
            sys.exit(1)

        chan.send("Welcome to dzh's fake SSH shell!\r\n\r\n")
        std_out = chan.makefile("a+")

        if usr_ == "root":
            fonts = "root@" + ip_str + "/# "
        else:
            fonts = usr_ + "@" + ip_str + ":~$ "

        def getSentence(visible=True):
            if visible:
                std_out.write(fonts)
            tmp_bytes = b""
            while True:
                command = chan.recv(1)
                if command == b"\r":
                    std_out.write(command)
                    std_out.write("\n")
                    break
                elif command == b"\x7f":
                    if len(tmp_bytes) == 0:
                        continue
                    if visible:
                        std_out.write("\b \b")
                    tmp_bytes = tmp_bytes[0: len(tmp_bytes) - 1]
                else:
                    tmp_bytes = tmp_bytes + command
                    # chan.send(command)
                    if visible:
                        std_out.write(command)
                    continue
            sentence = tmp_bytes.decode()
            print(sentence)
            if sentence == "":
                getSentence()
            return sentence

        def response(sentence):
            command_dispatcher.import_command()
            res = command_dispatcher.parseCommand(sentence)
            if res:
                std_out.write(res)
            else:
                with open("buffer", "r") as f:
                    r = f.readlines()
                    for line in r:
                        std_out.write(line + "\r")

        u_ = str(uuid.uuid4())[0:5]
        with open("control", "w") as f1:
            f1.write("1")

        while True:
            with open("thread_control/" + "pts" + str(thread_id), "r") as f:
                r = f.read()
                if r == "1":
                    break

            with open("control", "r") as f:
                r = f.read()
                if r != "1":
                    psw1 = getSentence(visible=False)
                    std_out.write("Permission denied, please try again.\r\n")
                    std_out.write(r + "'s password:")
                    print("get password:" + psw1)
                    log(psw1, addr, "id-" + u_ + "-psw-" + str(addr[0]) + "-" + r + ".txt")

                    psw2 = getSentence(visible=False)
                    std_out.write("Permission denied, please try again.\r\n")
                    std_out.write(r + "'s password:")
                    print("get password:" + psw2)
                    log(psw2, addr, "id-" + u_ + "-psw-" + str(addr[0]) + "-" + r + ".txt")

                    psw3 = getSentence(visible=False)
                    std_out.write(r + ": Permission denied (publickey,password).\r\n")
                    print("get password:" + psw3)
                    log(psw3, addr, "id-" + u_ + "-psw-" + str(addr[0]) + "-" + r + ".txt")

                    with open("control", "w") as f1:
                        f1.write("1")
            command = getSentence()
            log(command, addr, "id-" + u_ + "-ip-" + str(addr[0]) + ".txt")
            response(command)

        chan.close()
        sock.close()

    except Exception as e:
        print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)


if __name__ == "__main__":
    createServer("test_rsa.key", usr_="dzh", psw_="123456dzh", address=("", 2222))
