import requests
from django.shortcuts import render
import socket
from . import forms


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def login(request):
    if request.method == 'POST':
        UserLoginForm = forms.UserLoginForm(request.POST)
        if UserLoginForm.is_valid():
            username = UserLoginForm.cleaned_data.get('username')
            password = UserLoginForm.cleaned_data.get('password')
            ip = get_ip(request)
            url = 'http://10.21.196.121/webHoneyPot/'
            potID = socket.gethostname().split("Web")[1]
            data = {'ip': ip, 'username': username, 'password': password, 'potID': potID}
            requests.post(url, data)
        message = "账户或密码错误！"
        return render(request, "index.html", {'message': message})
    else:
        return render(request, "index.html")
