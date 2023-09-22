from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    money = models.IntegerField(default=1500)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class ChanceCard(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description

class CommunityChestCard(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description
