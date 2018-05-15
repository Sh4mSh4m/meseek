from django.urls import path, include
from django.contrib import admin
from . import views


app_name = 'chat'

urlpatterns = [
    # Index ex: /chat/
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('gettoken/', views.gettoken, name='gettoken'),
    path('mail/', views.mail, name='mail')
]