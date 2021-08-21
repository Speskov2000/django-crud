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
    path('products/', views.products),
    path('products/<int:productid>/', views.products),

    path('',views.index),
    path('test',views.test),

    re_path('^users/(?P<id>\d+)/(?P<name>\w+)/(?P<age>\d+)', views.users),
    re_path('^users/(?P<id>\d+)/(?P<name>\w+)', views.users),
    re_path('^users/(?P<id>\d+)', views.users),
    re_path('^users/', views.users),

    path('about/', TemplateView.as_view(template_name="templateView/about.html")),
    path('contact/', TemplateView.as_view(template_name="templateView/contact.html")),

    path('admin/', admin.site.urls),
]
