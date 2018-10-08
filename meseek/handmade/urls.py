from django.urls import path, include
from django.contrib import admin
from . import views


app_name = 'handmade'

urlpatterns = [
    # Index ex: /chat/
    path('', views.index, name='index'),
]