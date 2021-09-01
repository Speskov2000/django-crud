from django.db import models
# from django.contrib.auth import

# Проверить условие в all()

class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()

class Product(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    price = models.IntegerField()




