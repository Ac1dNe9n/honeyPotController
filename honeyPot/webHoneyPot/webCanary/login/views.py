import requests
from django.shortcuts import render
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
            print(ip)
            url = 'http://10.22.145.106/webHoneyPot/'
            data = {'ip': ip, 'username': username, 'password': password, 'potID': 1}
            r = requests.post(url, data)
            print(r.status_code)
        message = "账户或密码错误！"
        return render(request, "index.html", {'message': message})
    else:
        return render(request, "index.html")
