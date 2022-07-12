from os import access
from django.db import models

# Create your models here.


class Auth_user(models.Model):
    access_token = models.CharField(max_length=200)
    user_id = models.IntegerField()
