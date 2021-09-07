from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('register/', views.sign_up),
    path('login/', views.sign_in),
    path('logout/', views.sign_out),
]