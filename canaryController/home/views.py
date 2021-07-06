from datetime import datetime
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from . import forms, models


def index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    return render(request, "home/index.html")


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
    return render(request, 'home/statistics.html')


def source(request):
    return render(request, 'home/source.html')


def log(request):
    return render(request, 'home/threatLog.html')


def getOrigin(ip):
    r = requests.get("http://ip.taobao.com//outGetIpInfo?ip=%s" % ip)
    if r.json()['code'] == 0:
        i = r.json()['data']
        if i['city'] == '内网IP':
            return '局域网'
        return i['region']


@csrf_exempt
def webHoneyPort(request):
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
