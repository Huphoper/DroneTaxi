"""dronetaxi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from login import views
from django.urls import path, include

handler404 = views.Custom_handler404
urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('', views.login),
    path('login', views.login, name='login'),
    path('profile/', views.profile),
    path('admin/', admin.site.urls),
    path('myorders/', views.myorders),
    path('userslist/', views.userslist),
    path('droneslist/', views.droneslist),
    path('editprofile/', views.editprofile),
    path('droneedit/', views.droneedit),
    path('orderedit/', views.orderedit),
    path('orderadd/', views.orderadd),
    path('useradd/', views.useradd),
    path('droneadd/', views.droneadd),
]
