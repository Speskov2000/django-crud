from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render


def index(request):
    header = "Personal Data"                    # обычная переменная
    langs = ["English", "German", "Spanish"]    # массив
    user ={"name" : "Tom", "age" : 23}          # словарь
    addr = ("Абрикосовая", 23, 45)              # кортеж
 
    data = {"header": header, "langs": langs, "user": user, "address": addr}
    return render(request, "firstapp/index.html", context=data)


def products(request, productid=3):
    output = f"<h2>Product № {productid}</h2>"
    return HttpResponse(output)


def test(request):
    qwe = request.GET.get("qwe", "default?")

    output = f"qwe = {qwe}"
    return HttpResponse(output)


def users(request, id=1, name="bob", age=18):
    output = f"<h2>User</h2><h3>id: {id}  name: {name}, age: {age}</h3>"
    var = request.GET.get("name", "defalult")
    output += f" {var}"
    return HttpResponse(output)


def contact(request):
    return HttpResponseRedirect("/products")


def details(request):
    return HttpResponsePermanentRedirect("/")