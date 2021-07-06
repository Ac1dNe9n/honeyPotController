from django import forms
from captcha.fields import CaptchaField


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    captcha = CaptchaField()


class WebHoneyPotForm(forms.Form):
    ip = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
    potID = forms.IntegerField()
