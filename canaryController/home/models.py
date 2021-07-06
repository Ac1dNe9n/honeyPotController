from django.db import models


class ThreatType(models.Model):
    threatID = models.IntegerField(primary_key=True)
    num = models.IntegerField()


class ThreatIP(models.Model):
    ip = models.CharField(max_length=30, primary_key=True)
    origin = models.CharField(max_length=100)
    num = models.IntegerField()


class Threat(models.Model):
    id = models.AutoField(primary_key=True)
    honeyPotID = models.IntegerField()
    honeyPotType = models.IntegerField()
    ip = models.CharField(max_length=30)
    origin = models.CharField(max_length=100)
    time = models.CharField(max_length=30)
    detail = models.TextField()
