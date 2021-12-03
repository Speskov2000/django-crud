import jwt
import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from learnDjango.settings import SIMPLE_JWT

BASE_URL = "http://127.0.0.1:8088/"


def test(request):
    # a = 1/0
    return HttpResponse("Ответ")


def getTokens(request):
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
            # response = HttpResponseRedirect(f'\
            #         <a href="/jwt">Вернуться на главную<a>\
            #         <br>Access token: {access} <br>\
            #         Refresh token: {refresh}')
            response = HttpResponseRedirect('/jwt')
            response.set_cookie('access', access)
            response.set_cookie('refresh', refresh)
            return response
        else:
            return HttpResponse("Что-то пошло не так")
    else:
        return render(request, "jwtAuth/login.html")


def __checkValidToken(request, url):
    try:
        access = request.COOKIES.get('access')
        decodedToken = jwt.decode(
            access,
            SIMPLE_JWT['SIGNING_KEY'],
            algorithms=[SIMPLE_JWT['ALGORITHM']]
        )
        print("получилось декодировать токен. Вот он: ", decodedToken)
    except jwt.ExpiredSignatureError:
        __refreshToken(request, url)


def __refreshToken(request, url):
    '''Обновление access с помощью refresh'''
    refresh = request.COOKIES.get('refresh')
    r = requests.post(
        f'{BASE_URL}auth/jwt/refresh',
        data={
            'refresh': refresh
        }
    )
    if r.status_code == 200:
        access = r.json()['access']
        response = HttpResponse(f'<script>location = "{url}";</script>')

        response.set_cookie('access', access)
        print(f"Вы успешно обновили аксес токен: {access}")
        return response
    else:
        return HttpResponseRedirect('/jwt/getTokens')


# Create your views here.
def index(request):
    __checkValidToken(request, '/jwt')
    token = request.COOKIES.get('access')
    r = requests.get(
        f'{BASE_URL}auth/users/me',
        headers={
            'Authorization': f'JWT {token}',
        }
    )
    userInfo = ""
    if r.status_code == 200:
        userInfo = r.text
        return render(request, "jwtAuth/index.html", {'token': userInfo})
    return HttpResponse('токен каким-то образом не отработал')


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
        if token:
            return __refreshToken(request, '/jwt/about')
        else:
            return HttpResponseRedirect('/jwt/getTokens')

    return render(request, "jwtAuth/index.html", {'token': token})


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
            return HttpResponseRedirect("/jwt/getTokens")
        else:
            return HttpResponse("Не удалось создать пользователя")
    else:
        return render(request, "jwtAuth/register.html")
