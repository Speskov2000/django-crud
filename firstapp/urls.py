from django.urls import path
from . import views

app_name = 'firstapp'
urlpatterns = [
    path('createProduct/', views.createProduct),
    path('updateProduct/<int:id>/', views.updateProduct),
    path('deleteProduct/<int:id>/', views.deleteProduct),
]