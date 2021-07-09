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


class RDPHoneyPotForm(forms.Form):
    ip = forms.CharField()
    port = forms.CharField()
    ConnectTime = forms.CharField()
    DisconnectTime = forms.CharField()
    fileName = forms.CharField()


class RDPHoneyPotConnectForm(forms.Form):
    ip = forms.CharField()
    port = forms.CharField()
    ConnectTime = forms.CharField()
    DisconnectTime = forms.CharField()


class deleteForm(forms.Form):
    logID = forms.IntegerField()


class managePotForm(forms.Form):
    potID = forms.IntegerField()


class addForm(forms.Form):
    potType = forms.IntegerField()
    port = forms.CharField()


class addInForm(forms.Form):
    potType = forms.IntegerField()


class addSSHFrom(forms.Form):
    potType = forms.IntegerField()
    port = forms.CharField()
    ip = forms.CharField()
    username = forms.CharField()
    passwd = forms.CharField()
