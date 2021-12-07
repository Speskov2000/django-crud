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
    def wrapper(*args, **kwargs):
        try:
            if 'jwtUser' not in args[0].session:
                print("Вы не залогинились")
                return HttpResponseRedirect('/jwt/getTokens')

            if 'access' in args[0].session['jwtUser']:
                access = args[0].session['jwtUser']['access']
                decodedToken = jwt.decode(
                    access,
                    SIMPLE_JWT['SIGNING_KEY'],
                    algorithms=[SIMPLE_JWT['ALGORITHM']]
                )
                print("Получилось декодировать токен. Вот он: ", decodedToken)
                args[0].session['jwtUser']['auth'] = True
                print('все хорошо', args[0].session['jwtUser']['auth'])
                return func(*args, **kwargs)
            else:
                print("Access-token не задан. Пробуем обновить")
                args[0].session['jwtUser']['auth'] = False
                return __refreshToken(*args, func=func)
        except jwt.ExpiredSignatureError:
            print("Токен протух. Пробуем обновить")
            args[0].session['jwtUser']['auth'] = False
            return __refreshToken(*args, func=func)
    return wrapper


def __refreshToken(*args, **kwargs):
    '''Обновление access с помощью refresh'''

    if 'refresh' in args[0].session['jwtUser']:
        refresh = args[0].session['jwtUser']['refresh']
        r = requests.post(
            f'{BASE_URL}auth/jwt/refresh',
            data={'refresh': refresh}
        )
        if r.status_code == 200:
            args[0].session['jwtUser']['access'] = r.json()['access']
            print(f"Вы успешно обновили access-token:\
                    {args[0].session['jwtUser']['access']}")
            args[0].session['jwtUser']['auth'] = True
            return kwargs['func'](*args)
        else:
            print("Не получилось обновить токен - залогиньтесь")
            args[0].session['jwtUser']['auth'] = False
            return HttpResponseRedirect('/jwt/getTokens')
    print("У вас не заданы токены - залогиньтесь")
    args[0].session['jwtUser']['auth'] = False
    return HttpResponseRedirect('/jwt/getTokens')
