import jwt
from functools import wraps
import requests
from django.http import HttpResponseRedirect
from learnDjango.settings import SIMPLE_JWT

BASE_URL = "http://127.0.0.1:8088/"


def isTokenValid(func):
    '''Декоратор для проверки валидности токена
    и рефреша его в случае необходимости'''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            if 'access' in request.session['jwtUser']:
                access = request.session['jwtUser']['access']
                print("Декодируем текущий токен:")
                print(access)
                jwt.decode(
                    access,
                    SIMPLE_JWT['SIGNING_KEY'],
                    algorithms=[SIMPLE_JWT['ALGORITHM']]
                )
                print("Получилось декодировать токен.")
                request.session['jwtUser']['auth'] = True
                request.session.modified = True
                return func(request, *args, **kwargs)
            else:
                print("Access-token не задан. Пробуем обновить")
                return __refreshToken(request, func, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            print("Токен протух. Пробуем обновить")
            return __refreshToken(request, func, *args, **kwargs)
    return wrapper


def __refreshToken(request, func, *args, **kwargs):
    '''Обновление access с помощью refresh'''
    request.session['jwtUser']['auth'] = False

    if 'refresh' in request.session['jwtUser']:
        refresh = request.session['jwtUser']['refresh']
        r = requests.post(
            f'{BASE_URL}auth/jwt/refresh',
            data={'refresh': refresh}
        )
        if r.status_code == 200:
            request.session['jwtUser']['access'] = r.json()['access']
            print("Был записан новый access-token:")
            print(request.session['jwtUser']['access'])
            request.session['jwtUser']['auth'] = True
            request.session.modified = True
            return func(request, *args, **kwargs)
        else:
            print("Не получилось обновить токен - залогиньтесь")
            return HttpResponseRedirect('/jwt/getTokens')
    print("У вас не заданы токены - залогиньтесь")
    return HttpResponseRedirect('/jwt/getTokens')
