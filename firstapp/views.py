from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render


def index(request):
    header = "Personal Data"  # обычная переменная
    langs = ["English", "German", "Spanish"]  # массив
    user = {"name": "Tom", "age": 23}  # словарь
    addr = ("Абрикосовая", 23, 45)  # кортеж

    data = {"header": header, "langs": langs, "user": user, "address": addr}
    return render(request, "firstapp/index.html", context=data)


def user(request, id=1, name="bob", age=18):
    data = {"id": id, "name": name, "age": age}
    return render(request, "firstapp/user.html", context=data)


def contact(request):
    return HttpResponseRedirect("/products")


def details(request):
    return HttpResponsePermanentRedirect("/")