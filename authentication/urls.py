from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('createUser/', views.createUser),
    path('updateUser/<int:id>/', views.updateUser),
    path('deleteUser/<int:id>/', views.deleteUser),
]