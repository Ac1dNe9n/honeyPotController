from django import forms
from captcha.fields import CaptchaField


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    captcha = CaptchaField()


class MysqlHoneyPot(forms.Form):
    ip = forms.CharField()
    file = forms.CharField()
    potID = forms.IntegerField()


class WebHoneyPotForm(forms.Form):
    ip = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
    potID = forms.IntegerField()


class deleteForm(forms.Form):
    logID = forms.IntegerField()
