from django.db import models

# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ", " + self.country
