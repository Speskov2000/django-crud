BASE_URL = "http://127.0.0.1:8088/"


class JwtMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if 'jwtUser' not in request.session:
            request.session['jwtUser'] = {'auth': False}
        response = self._get_response(request)
        return response

    # def process_exception(self, request, exception):
    #     print(f'Exception is {exception}')
    #     return HttpResponse('Exception')
