from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def sign_up(request):
    if request.method == "POST":
        regForm = UserCreationForm(request.POST)
        if regForm.is_valid():
            user = regForm.save()
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(
                    request,
                    "authentication/register.html",
                    {"form": regForm})
    else:
        return render(
                request,
                "authentication/register.html",
                {"form": UserCreationForm()})


def sign_in(request):
    if request.method == "POST":
        authForm = AuthenticationForm(data=request.POST)
        if authForm.is_valid():
            user = authForm.get_user()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    return HttpResponse("Вы деактивировали ваш аккаунт")
            else:
                return HttpResponse("Такого пользователя не существует")
        else:
            return render(
                    request, "authentication/login.html", {"form": authForm})
    else:
        return render(
                request,
                "authentication/login.html",
                {"form": AuthenticationForm()})


def sign_out(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

