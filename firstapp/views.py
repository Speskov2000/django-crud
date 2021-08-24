from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from .forms import UserForm
from .models import Person


# получение данных из бд
def index(request):
    people = Person.objects.all()
    return render(request, "firstapp/index.html", {"people": people})


# сохранение данных в бд
def create(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            person = Person()
            person.name = userform.cleaned_data["name"]
            person.age = userform.cleaned_data["age"]
            person.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "firstapp/create.html", {"form": userform})
    else:
        return render(request, "firstapp/create.html", {"form": UserForm()})


def update(request, id):
    try:
        person = Person.objects.get(id=id)

        if request.method == "POST":
            userform = UserForm(request.POST)
            if userform.is_valid():
                person.name = userform.cleaned_data["name"]
                person.age = userform.cleaned_data["age"]
                person.save(update_fields=["name", "age"])
                return HttpResponseRedirect("/")
            else:
                return render(request, "firstapp/create.html", {"form": userform})
        else:
            userform = UserForm(initial={
                "name": person.name,
                "age": person.age
            })
            return render(request, "firstapp/update.html", {"form": userform})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def delete(request, id):
    try:
        Person.objects.filter(id=id).delete()
        return HttpResponseRedirect("/")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def contact(request):
    # return HttpResponseRedirect("/products")
    users = Person.objects.all()


def details(request):
    return HttpResponsePermanentRedirect("/")