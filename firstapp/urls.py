from django.urls import path
from . import views

app_name = 'firstapp'
urlpatterns = [
    path('', views.index),
    path('ofUser/<int:userId>/', views.ofUser),
    path('create/', views.create),
    path('update/<int:id>/', views.update),
    path('delete/<int:id>/', views.delete),
]
