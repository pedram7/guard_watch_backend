from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class MyUser(AbstractUser):
    isOperator = models.BooleanField(default=False)


class Guard(models.Model):
    name = models.CharField(max_length=255)
    staff_id = models.CharField(max_length=255, unique=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    date_left = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} : {}".format(self.name, self.staff_id)


class Wristband(models.Model):
    band_id = models.CharField(max_length=255, unique=True)
    guard = models.OneToOneField(Guard, on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                 related_name='band')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "band {}".format(self.band_id)


class LogInstance(models.Model):
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lang = models.DecimalField(max_digits=10, decimal_places=7)
    wristband = models.ForeignKey(Wristband, on_delete=models.CASCADE)
    guard = models.ForeignKey(Guard, on_delete=models.SET_NULL, blank=True, null=True)
    time = models.DateTimeField()
    heartbeat = models.PositiveSmallIntegerField(blank=True, null=True)
    emergency_alert = models.BooleanField(default=False)

    def __str__(self):
        return "log for band {} on {}".format(self.wristband.band_id, self.time)

    class Meta:
        unique_together = ('time', 'wristband')
