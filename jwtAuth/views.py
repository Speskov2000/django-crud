import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from learnDjango.views import isTokenValid


BASE_URL = "http://127.0.0.1:8088/"


def getTokens(request):
    '''Необходима для запроса токена с сервиса auth и авторизации'''

    if request.method == 'POST':
        r = requests.post(
            f'{BASE_URL}auth/jwt/create',
            data={
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
            }
        )
        if r.status_code == 200:
            request.session['jwtUser'] = {
                    'access': r.json()['access'],
                    'refresh': r.json()['refresh'],
                    'auth': True,
                    'user_id': r.json()['user_id'],
                    'user_name': r.json()['user_name'],
                }
            print(request.session['jwtUser'])
            return HttpResponseRedirect("/jwt")
        else:
            return HttpResponse("Что-то пошло не так. Логин или пароль.\
                    А может интернет. А может сервис auth лег")
    else:
        return render(request, "jwtAuth/login.html")


def delTokens(request):
    '''Что-то в духе logout'a'''
    if 'jwtUser' in request.session:
        del request.session['jwtUser']
    return HttpResponseRedirect("/")


@isTokenValid
def index(request):
    token = request.session['jwtUser']['access']
    r = requests.get(
        f'{BASE_URL}auth/users/me',
        headers={
            'Authorization': f'JWT {token}',
        }
    )
    userInfo = ""
    if r.status_code == 200:
        userInfo = r.text
        return render(request, "jwtAuth/index.html", {'json_info': userInfo})
    return HttpResponse('токен каким-то образом не отработал')


@isTokenValid
def about(request):
    token = request.session['jwtUser']['access']
    r = requests.get(
        f'{BASE_URL}about',
        headers={
            'Authorization': f'JWT {token}',
        }
    )
    if r.status_code == 200:
        aboutText = r.text
        return render(request, "jwtAuth/index.html", {'json_info': aboutText})
    else:
        return HttpResponse('токен каким-то образом не отработал')


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
            return HttpResponseRedirect("/jwt/getTokens")
        else:
            return HttpResponse("Не удалось создать пользователя")
    else:
        return render(request, "jwtAuth/register.html")
