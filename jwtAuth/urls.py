from django.urls import path
from . import views

app_name = 'jwtAuth'
urlpatterns = [
    path('', views.index),
    path('about', views.about),
    path('getTokens', views.getTokens),
    path('register', views.createUser),
]
