from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, logout

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        # email = regForm.cleaned_data["email"]
        password = request.POST.get("password")
        user = User.objects.create_user(username, username, password)
        # login(request, user)
        return HttpResponseRedirect("/")
        # regForm = UserCreationForm(request.POST)
        # if regForm.is_valid():
        #     username = regForm.cleaned_data["username"]
        #     # email = regForm.cleaned_data["email"]
        #     password = regForm.cleaned_data["password"]
        #     user = User.objects.create_user(username, password)
        #     login(request, user)
        #     return HttpResponseRedirect("/")
        # else:
        #     return render(request, "authentication/register.html", {"form": regForm})
    else:
        return render(request, "authentication/register.html", {"form": UserCreationForm()})

def login(request):
    if request.method == "POST":
        authForm = AuthenticationForm(request.POST)
        # if authForm.is_valid():
            # username = authForm.cleaned_data["username"]
            # password = authForm.cleaned_data["password"]
        username = request.POST.get("username")
        # email = regForm.cleaned_data["email"]
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("Вы деактивировали ваш аккаунт")
        else:
            return render(request, "authentication/login.html", {"form": authForm})
    else:
        return render(request, "authentication/login.html", {"form": AuthenticationForm()})


def logout(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")