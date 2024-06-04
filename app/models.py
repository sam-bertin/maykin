from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class City(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    address = models.TextField(null=True)
    image = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
