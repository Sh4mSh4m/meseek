from django.urls import path, include
from . import views


app_name = 'nadeshiko'

urlpatterns = [
    # Index ex: /nadeshiko/
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('my_account/<int:user_id>', views.my_account, name='my_account'),
    path('hiraganas/', views.hiraganas, name='hiraganas'),
    path('katakanas/', views.katakanas, name='katakanas'),
]