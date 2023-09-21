from django.db import models
from django.utils import timezone

class Property(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    owner = models.ForeignKey('Player', on_delete=models.CASCADE, null=True, blank=True)

class Player(models.Model):
    name = models.CharField(max_length=100)
    money = models.IntegerField(default=1500)
    position = models.IntegerField(default=0)
