# from django.conf import settings
from django.db import models


class Product(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=40)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
