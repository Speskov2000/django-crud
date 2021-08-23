from django.db import models

# Проверить условие в all()

class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()

