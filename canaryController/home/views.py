from datetime import datetime
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from . import forms, models
import socket
import rsa
import pickle
from cryptography.fernet import Fernet
import hashlib


def index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    honeyPots = models.HoneyPots.objects.all().values_list("honeyPotID", "honeyPotType", "ThreatNum", "status",
                                                           "IsIntranet")
    pots = []
    for p in honeyPots:
        pots.append({'honeyPotID': p[0], 'honeyPotType': getHoneyPotType(p[1]), 'ThreatNum': p[2], "status": p[3],
                     "IsIntranet": p[4]})
    return render(request, "home/index.html", {"pots": pots})


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/')
    if request.method == 'POST':
        UserLoginForm = forms.UserLoginForm(request.POST)
        if UserLoginForm.is_valid():
            username = UserLoginForm.cleaned_data.get('username')
            password = UserLoginForm.cleaned_data.get('password')
            if username == 'admin' and password == 'zx123456':
                request.session['is_login'] = True
                return redirect('/')
            else:
                message = '密码不正确！'
                return render(request, 'home/login.html', {'UserLoginForm': UserLoginForm, 'message': message})
        else:
            message = '验证码有误！'
            return render(request, 'home/login.html', {'UserLoginForm': UserLoginForm, 'message': message})
    else:
        UserLoginForm = forms.UserLoginForm()
        return render(request, 'home/login.html', {'UserLoginForm': UserLoginForm})


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


def statistics(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    data = models.ThreatType.objects.all().values_list("num")
    data1 = models.Threat.objects.all().values_list("time")
    temp = []
    countnum = [0] * 6
    nowtime = datetime.now().strftime("%Y-%m-%d")
    print(nowtime)
    for i in data:
        temp.append(i[0])
    for k in data1:
        datatemp = k[0]
        if datatemp[:10] == nowtime:
            if datatemp[11:13] == "0" or datatemp[11:13] == "01" or datatemp[11:13] == "02" or datatemp[
                                                                                               11:13] == "03":
                countnum[0] += 1
            elif datatemp[11:13] == "04" or datatemp[11:13] == "05" or datatemp[11:13] == "06" or datatemp[
                                                                                                  11:13] == "07":
                countnum[1] += 1
            elif datatemp[11:13] == "08" or datatemp[11:13] == "09" or datatemp[11:13] == "10" or datatemp[
                                                                                                  11:13] == "11":
                countnum[2] += 1
            elif datatemp[11:13] == "12" or datatemp[11:13] == "13" or datatemp[11:13] == "14" or datatemp[
                                                                                                  11:13] == "15":
                countnum[3] += 1
            elif datatemp[11:13] == "16" or datatemp[11:13] == "17" or datatemp[11:13] == "18" or datatemp[
                                                                                                  11:13] == "19":
                countnum[4] += 1
            elif datatemp[11:13] == "20" or datatemp[11:13] == "21" or datatemp[11:13] == "22" or datatemp[
                                                                                                  11:13] == "23":
                countnum[5] += 1
    countnum[1] += countnum[0]
    countnum[2] += countnum[1]
    countnum[3] += countnum[2]
    countnum[4] += countnum[3]
    countnum[5] += countnum[4]
    return render(request, 'home/statistics.html', {'attackData': temp, 'attacktime': countnum})


def inList(name, l):
    count = 0
    for i in l:
        if name == i:
            return count
        count += 1
    return -1


def source(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    data = models.ThreatIP.objects.all().order_by("-num").values_list('ip', 'origin', 'num')
    originName = []
    originNum = []
    attackerIP = []
    attackerNum = []
    count = 0
    for i in data:
        if count < 5:
            attackerIP.append(i[0])
            attackerNum.append(i[2])
        count += 1
        o = i[1]
        index = inList(o, originName)
        if index == -1:
            originName.append(o)
            originNum.append(i[2])
        else:
            originNum[index] += i[2]
    print("ok")
    return render(request, 'home/source.html',
                  {'attackerIP': attackerIP, 'attackerNum': attackerNum, 'originName': originName,
                   'originNum': originNum})


def getHoneyPotType(t):
    if t == 1:
        return "Web"
    elif t == 2:
        return "Mysql1"
    elif t == 3:
        return "Mysql2"
    elif t == 4:
        return "SSH高仿真"
    elif t == 5:
        return "RDP"
    elif t == 6:
        return "SSH环境"
    elif t == 7:
        return "内网WEB"
    elif t == 8:
        return "内网数据库"
    else:
        return "其他"


def log(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == "POST":
        logForm = forms.deleteForm(request.POST)
        if logForm.is_valid():
            logID = logForm.cleaned_data.get('logID')
            models.Threat.objects.filter(id=logID).delete()
    data = models.Threat.objects.all().values_list('honeyPotID', 'honeyPotType', 'ip', 'origin', 'time', 'detail',
                                                   'id')
    lg = []
    for i in data:
        lg.append(
            {'honeyPotID': i[0], 'honeyPotType': getHoneyPotType(i[1]), 'ip': i[2], 'origin': i[3], 'time': i[4],
             'detail': i[5], 'id': i[6]})
    return render(request, 'home/threatLog.html', {'log': lg})


def about(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    return render(request, 'home/about.html')


def getOrigin(ip):
    r = requests.get("http://ip.taobao.com//outGetIpInfo?ip=%s" % ip)
    if r.json()['code'] == 0:
        i = r.json()['data']
        if i['city'] == '内网IP':
            return '局域网'
        return i['region']


def addOutPot(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == 'POST':
        addSSHForm = forms.addSSHFrom(request.POST)
        if addSSHForm.is_valid():
            potType = addSSHForm.cleaned_data.get('potType')
            username = addSSHForm.cleaned_data.get('username')
            passwd = addSSHForm.cleaned_data.get('passwd')
            port = addSSHForm.cleaned_data.get('port')
            ip = addSSHForm.cleaned_data.get('ip')
            temp = models.HoneyPots.objects.create(honeyPotType=potType, ThreatNum=0, status=1, IsIntranet=False)
            id = temp.honeyPotID
        else:
            manageForm = forms.addForm(request.POST)
            if manageForm.is_valid():
                potType = manageForm.cleaned_data.get('potType')
                temp = models.HoneyPots.objects.create(honeyPotType=potType, ThreatNum=0, status=1, IsIntranet=False)
                id = temp.honeyPotID
    return redirect("/")


def delPot(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == 'POST':
        manageForm = forms.managePotForm(request.POST)
        if manageForm.is_valid():
            potID = manageForm.cleaned_data.get('potID')
            models.HoneyPots.objects.filter(honeyPotID=potID).delete()
    return redirect("/")


def resetPot(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == 'POST':
        manageForm = forms.managePotForm(request.POST)
        if manageForm.is_valid():
            potID = manageForm.cleaned_data.get('potID')
    return redirect("/")


@csrf_exempt
def mysqlHoneyPot(request):
    if request.method == 'POST':
        MysqlHoneyPot = forms.MysqlHoneyPot(request.POST)
        if MysqlHoneyPot.is_valid():
            ip = MysqlHoneyPot.cleaned_data.get('ip')
            origin = getOrigin(ip)
            file = MysqlHoneyPot.cleaned_data.get('file')
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            honeyPotID = int(MysqlHoneyPot.cleaned_data.get('potID'))
            honeyPotType = 2
            detail = "IP:" + ip + "尝试攻击mysql数据库,已获取其/etc/passwd文件,文件内容为：              " + file
            models.Threat.objects.create(honeyPotID=honeyPotID, honeyPotType=honeyPotType, ip=ip, origin=origin,
                                         time=now
                                         , detail=detail)
            t = models.ThreatType.objects.filter(threatID=2)
            if t:
                t.update(num=t[0].num + 1)
            tip = models.ThreatIP.objects.filter(ip=ip)
            if tip.exists():
                tip.update(num=tip[0].num + 1)
            else:
                models.ThreatIP.objects.create(ip=ip, origin=origin, num=1)
    return HttpResponse()


@csrf_exempt
def webHoneyPot(request):
    if request.method == 'POST':
        WebHoneyPotForm = forms.WebHoneyPotForm(request.POST)
        if WebHoneyPotForm.is_valid():
            ip = WebHoneyPotForm.cleaned_data.get('ip')
            origin = getOrigin(ip)
            honeyPotID = WebHoneyPotForm.cleaned_data.get('potID')
            username = WebHoneyPotForm.cleaned_data.get('username')
            password = WebHoneyPotForm.cleaned_data.get('password')
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            honeyPotType = 1
            detail = "非法密码尝试\n用户名：" + username + "\n密码: " + password
            models.Threat.objects.create(honeyPotID=honeyPotID, honeyPotType=honeyPotType, ip=ip, origin=origin,
                                         time=now
                                         , detail=detail)
            t = models.ThreatType.objects.filter(threatID=1)
            if t:
                t.update(num=t[0].num + 1)
            tip = models.ThreatIP.objects.filter(ip=ip)
            if tip.exists():
                tip.update(num=tip[0].num + 1)
            else:
                models.ThreatIP.objects.create(ip=ip, origin=origin, num=1)
    return HttpResponse()


# mode: 1 添加 2 删除 3 重置
def sendSSH1Data(addr, data):
    asyKey = rsa.newkeys(2048)
    # 公钥和私钥
    publicKey = asyKey[0]
    privateKey = asyKey[1]
    # 创建socket通信对象
    # 默认使用AF_INET协议族，即ipv4地址和端口号的组合以及tcp协议
    clientSocket = socket.socket()
    # 默认连接服务器地址为本机ip和8080端口
    clientSocket.connect(addr)

    # 向服务器传递公钥，和该公钥字符串化后的sha256值
    print("正在向服务器传送公钥")
    sendKey = pickle.dumps(publicKey)
    sendKeySha256 = hashlib.sha256(sendKey).hexdigest()
    clientSocket.send(pickle.dumps((sendKey, sendKeySha256)))

    # 接受服务器传递的密钥并进行解密
    symKey, symKeySha256 = pickle.loads(clientSocket.recv(1024))
    if hashlib.sha256(symKey).hexdigest() != symKeySha256:
        print("error")
    else:
        print("密钥交换完成")
        symKey = pickle.loads(rsa.decrypt(symKey, privateKey))
    # 初始化加密对象
    f = Fernet(symKey)
    en_sendData = f.encrypt(data.encode())
    clientSocket.send(en_sendData)
    en_recvData = clientSocket.recv(1024)
    recvData = f.decrypt(en_recvData).decode()
    print("接受到服务器传来的消息：{0}".format(recvData))
