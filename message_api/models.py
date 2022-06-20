from django.db import models
from django.contrib.auth.models import User



class Audience(models.Model):
    name = models.CharField(max_length = 180)

    def __str__(self):
        return f"ID : {self.id} , NAME : {self.name} "


class Account(models.Model):
    user_id = models.CharField(max_length = 180)
    group = models.ManyToManyField(Audience, blank = True, null = True)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return f"ID : {self.id} , USER_ID : {self.user_id} , GROUP : {self.group} , ADMIN : {self.is_admin}"