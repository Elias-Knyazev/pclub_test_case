from django.contrib.auth.models import User
from django.db import models


class EquipClub(models.Model):
    type = models.CharField(max_length=255)
    eq_number = models.IntegerField()
    rent_price = models.FloatField(default=0)
    hour_rent = models.IntegerField(default=0)
    time_rent_start = models.DateTimeField(auto_now=True)
    time_rent_end = models.DateTimeField(auto_now=True)
    is_busy = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class UserRent(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    last_hour_rent = models.IntegerField(default=0)
    hour_sum = models.IntegerField(default=0)
    discount = models.FloatField(default=1)





