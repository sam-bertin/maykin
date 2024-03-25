from django.db import models

# Create your models here.
class City(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE) # Delete all hotels in a city if city is deleted
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name