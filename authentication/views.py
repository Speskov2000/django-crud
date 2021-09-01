from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from firstapp.forms import UserForm
from firstapp.models import Person

def login():
    return HttpResponseRedirect("/")

def register():
    return HttpResponseRedirect("/")

# Create your views here.
# Создание нового пользователя
def createUser(request):
    if request.method == "POST":
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            person = Person()
            person.name = userForm.cleaned_data["name"]
            person.age = userForm.cleaned_data["age"]
            person.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "firstapp/createUser.html", {"form": userForm})
    else:
        return render(request, "firstapp/createUser.html", {"form": UserForm()})


# Обновление пользователя
def updateUser(request, id):
    try:
        person = Person.objects.get(id=id)

        if request.method == "POST":
            userForm = UserForm(request.POST)
            if userForm.is_valid():
                person.name = userForm.cleaned_data["name"]
                person.age = userForm.cleaned_data["age"]
                person.save(update_fields=["name", "age"])
                return HttpResponseRedirect("/")
            else:
                return render(request, "firstapp/updateUser.html", {"form": userForm})
        else:
            userForm = UserForm(initial={
                "name": person.name,
                "age": person.age
            })
            return render(request, "firstapp/updateUser.html", {"form": userForm})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# Удаление пользователя
def deleteUser(request, id):
    try:
        Person.objects.filter(id=id).delete()
        return HttpResponseRedirect("/")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")