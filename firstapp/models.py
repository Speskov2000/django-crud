# from django.conf import settings
from django.db import models


class Product(models.Model):
    userId = models.IntegerField(default=0)
    userName = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
