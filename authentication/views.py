from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def login(request):
    if request.method == "POST":
        userForm = UserForm_name(request.POST)
        if userForm.is_valid():
            username = userForm.cleaned_data["username"]
            password = userForm.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    return HttpResponse("Вы деактивировали ваш аккаунт")
        else:
            return render(request, "authentication/login.html", {"form": userForm})
    else:
        return render(request, "authentication/login.html", {"form": UserForm()})


def logout(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

def register(request):
    return HttpResponseRedirect("/")

def create(request):
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    return HttpResponseRedirect("/")

def update(request):
    request.user.save()
    return HttpResponseRedirect("/")

def delete(request):
    return HttpResponseRedirect("/")

# Create your views here.
# Создание нового пользователя
# def createUser(request):
#     if request.method == "POST":
#         userForm = UserForm(request.POST)
#         if userForm.is_valid():
#             person = Person()
#             person.name = userForm.cleaned_data["name"]
#             person.age = userForm.cleaned_data["age"]
#             person.save()
#             return HttpResponseRedirect("/")
#         else:
#             return render(request, "firstapp/createUser.html", {"form": userForm})
#     else:
#         return render(request, "firstapp/createUser.html", {"form": UserForm()})


# # Обновление пользователя
# def updateUser(request, id):
#     try:
#         person = Person.objects.get(id=id)

#         if request.method == "POST":
#             userForm = UserForm(request.POST)
#             if userForm.is_valid():
#                 person.name = userForm.cleaned_data["name"]
#                 person.age = userForm.cleaned_data["age"]
#                 person.save(update_fields=["name", "age"])
#                 return HttpResponseRedirect("/")
#             else:
#                 return render(request, "firstapp/updateUser.html", {"form": userForm})
#         else:
#             userForm = UserForm(initial={
#                 "name": person.name,
#                 "age": person.age
#             })
#             return render(request, "firstapp/updateUser.html", {"form": userForm})
#     except Person.DoesNotExist:
#         return HttpResponseNotFound("<h2>Person not found</h2>")


# # Удаление пользователя
# def deleteUser(request, id):
#     try:
#         Person.objects.filter(id=id).delete()
#         return HttpResponseRedirect("/")
#     except Person.DoesNotExist:
#         return HttpResponseNotFound("<h2>Person not found</h2>")