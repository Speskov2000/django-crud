from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('login/', views.login),
    path('logout/', views.login),
    path('register/', views.register),
    path('create/', views.createUser),
    path('update/', views.updateUser),
    path('delete/', views.deleteUser),
]