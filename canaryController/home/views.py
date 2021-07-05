from django.shortcuts import render, redirect
from . import forms




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
