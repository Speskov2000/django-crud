from django.conf import settings
from django.db import models


class Product(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
