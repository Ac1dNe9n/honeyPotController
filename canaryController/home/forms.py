from django import forms
from captcha.fields import CaptchaField


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    captcha = CaptchaField()
