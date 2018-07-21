from django.urls import path, include
from . import views


app_name = 'nadeshiko'

urlpatterns = [
    # Index ex: /nadeshiko/
    path('', views.index, name='index'),
]