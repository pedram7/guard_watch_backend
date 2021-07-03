from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class MyUser(AbstractUser):
    isOperator = models.BooleanField(default=False)


class Guard(models.Model):
    name = models.CharField(max_length=255)
    staff_id = models.CharField(max_length=255)
    date_joined = models.DateTimeField(blank=True, null=True)
    date_left = models.DateTimeField(blank=True, null=True)


class Wristband(models.Model):
    band_id = models.CharField(max_length=255)
    guard = models.ForeignKey(Guard, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)


class LogInstance(models.Model):
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lang = models.DecimalField(max_digits=10, decimal_places=7)
    wristband = models.ForeignKey(Wristband, on_delete=models.SET_NULL)
    guard = models.ForeignKey(Guard, on_delete=models.SET_NULL)
    time = models.DateTimeField(auto_now_add=True)
    heartbeat = models.PositiveSmallIntegerField(blank=True, null=True)
    emergency_alert = models.BooleanField(default=False)
