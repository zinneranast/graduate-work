from django.db import models

class Users(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    UserIP = models.CharField(max_length=15)
