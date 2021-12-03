import jwt
import requests
from django.http import HttpResponseRedirect, HttpResponse
from learnDjango.settings import SIMPLE_JWT

BASE_URL = "http://127.0.0.1:8088/"


class JwtMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        try:
            access = request.COOKIES.get('access')
            decodedToken = jwt.decode(
                access,
                SIMPLE_JWT['SIGNING_KEY'],
                algorithms=[SIMPLE_JWT['ALGORITHM']]
            )
            print("получилось декодировать токен. Вот он: ", decodedToken)
        except jwt.ExpiredSignatureError:
            refresh = request.COOKIES.get('refresh')
            if refresh:
                r = requests.post(
                    f'{BASE_URL}auth/jwt/refresh',
                    data={
                        'refresh': refresh
                    }
                )
                if r.status_code == 200:
                    access = r.json()['access']
                    response = HttpResponseRedirect("/jwt")

                    response.set_cookie('access', access)
                    print(f"Вы успешно обновили аксес токен: {access}")
                    return response
                else:
                    return HttpResponseRedirect('/jwt/getTokens')
            else:
                return HttpResponseRedirect('/jwt/getTokens')

        response = self._get_response(request)

        return response

    def process_exception(self, request, exception):
        print(f'Exception is {exception}')
        return HttpResponse('Exception')
