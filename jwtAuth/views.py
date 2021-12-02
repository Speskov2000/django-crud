import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

BASE_URL = "http://127.0.0.1:8088/"


# Create your views here.
def index(request):
    token = request.COOKIES.get('access')
    r = requests.get(
        f'{BASE_URL}auth/users/me',
        headers={
            'Authorization': f'JWT {token}',
        }
    )
    if r.status_code == 200:
        token = r.text
    elif r.status_code == 301:
        token = "Токен протух"
    else:
        token = "Вы не авторизованы"

    return render(request, "jwtAuth/index.html", {'token': token})


def about(request):
    token = request.COOKIES.get('access')
    r = requests.get(
        f'{BASE_URL}about',
        headers={
            'Authorization': f'JWT {token}',
        }
    )
    if r.status_code == 200:
        token = r.text
    else:
        token = "Вы не авторизованы"

    return render(request, "jwtAuth/index.html", {'token': token})


def getToken(request):
    '''Необходима для запроса токена с сервиса auth и авторизации'''
    if request.method == 'POST':
        r = requests.post(
            f'{BASE_URL}auth/jwt/create',
            data={
                'username': request.POST.get('username'),
                'password': request.POST.get('password')
            }
        )
        if r.status_code == 200:
            access = r.json()['access']
            refresh = r.json()['refresh']

            response = HttpResponse(f'Access token: {access} <br>\
                    Refresh token: {refresh}')
            response.set_cookie('access', access)
            response.set_cookie('refresh', refresh)
            return response
        else:
            return HttpResponse("Что-то пошло не так")
    else:
        return render(request, "jwtAuth/login.html")


def createUser(request):
    if request.method == 'POST':
        r = requests.post(
            f'{BASE_URL}auth/users/',
            data={
                'username': request.POST.get('username'),
                'password': request.POST.get('password')
            }
        )

        if r.status_code == 201:
            # return HttpResponse(r.json())
            return HttpResponseRedirect("/jwt/getToken")
        else:
            return HttpResponse("Не удалось создать пользователя")
    else:
        return render(request, "jwtAuth/register.html")
