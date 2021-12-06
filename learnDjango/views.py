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
    def wrapper(request):
        try:
            if 'jwtUser' not in request.session:
                print("Вы не залогинились")
                return HttpResponseRedirect('/jwt/getTokens')

            if 'access' in request.session['jwtUser']:
                access = request.session['jwtUser']['access']
                decodedToken = jwt.decode(
                    access,
                    SIMPLE_JWT['SIGNING_KEY'],
                    algorithms=[SIMPLE_JWT['ALGORITHM']]
                )
                print("Получилось декодировать токен. Вот он: ", decodedToken)
                request.session['jwtUser']['auth'] = True
                print('все хорошо', request.session['jwtUser']['auth'])
                return func(request)
            else:
                print("Access-token не задан. Пробуем обновить")
                request.session['jwtUser']['auth'] = False
                return __refreshToken(request, func)
        except jwt.ExpiredSignatureError:
            print("Токен протух. Пробуем обновить")
            request.session['jwtUser']['auth'] = False
            return __refreshToken(request, func)
    return wrapper


def __refreshToken(request, func):
    '''Обновление access с помощью refresh'''

    if 'refresh' in request.session['jwtUser']:
        refresh = request.session['jwtUser']['refresh']
        r = requests.post(
            f'{BASE_URL}auth/jwt/refresh',
            data={'refresh': refresh}
        )
        if r.status_code == 200:
            request.session['jwtUser']['access'] = r.json()['access']
            print(f"Вы успешно обновили access-token:\
                    {request.session['jwtUser']['access']}")
            request.session['jwtUser']['auth'] = True
            return func(request)
        else:
            print("Не получилось обновить токен - залогиньтесь")
            request.session['jwtUser']['auth'] = False
            return HttpResponseRedirect('/jwt/getTokens')
    print("У вас не заданы токены - залогиньтесь")
    request.session['jwtUser']['auth'] = False
    return HttpResponseRedirect('/jwt/getTokens')
