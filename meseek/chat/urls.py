from django.urls import path, include
from django.contrib import admin
from . import views


app_name = 'chat'

urlpatterns = [
    # Index ex: /chat/
    path('', views.index, name='index'),
]