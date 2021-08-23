from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from .forms import UserForm
from .models import Person


# получение данных из бд
def index(request):
    people = Person.objects.all()
    userform = UserForm()
    return render(request, "firstapp/index.html", {
        "form": userform,
        "people": people
    })


# сохранение данных в бд
def create(request):
    if request.method == "POST":
        tom = Person()
        tom.name = request.POST.get("name")
        tom.age = request.POST.get("age")
        tom.save()
    return HttpResponseRedirect("/")


def update(request, id):
    if request.method == "POST":
        tom = Person.objects.get(id=id)
        tom.name = request.POST.get("name")
        tom.age = request.POST.get("age")
        tom.save(update_fields=["name", "age"])
        return HttpResponseRedirect("/")
    else:
        userform = UserForm()
        user = Person.objects.get(id=id)
        return render(request, "firstapp/update.html", {"form": userform, "user": user})


def delete(request, id):
    if request.method == "POST":
        person = Person.objects.get(id=id)
        person.delete()
    return HttpResponseRedirect("/")


def contact(request):
    # return HttpResponseRedirect("/products")
    users = Person.objects.all()

    users


def details(request):
    return HttpResponsePermanentRedirect("/")