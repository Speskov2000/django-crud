"""learnDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from firstapp import views

urlpatterns = [
    path('', views.index),

    path('createUser/', views.createUser),
    path('updateUser/<int:id>/', views.updateUser),
    path('deleteUser/<int:id>/', views.deleteUser),

    path('productsOfUser/<int:userId>', views.productsOfUser),
    path('createProduct/', views.createProduct),
    path('updateProduct/<int:id>/', views.updateProduct),
    path('deleteProduct/<int:id>/', views.deleteProduct),

    path('admin/', admin.site.urls),
]
