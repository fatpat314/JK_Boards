from django.db import models

# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ", " + self.country

class Register(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.IntegerField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ", " + self.email
