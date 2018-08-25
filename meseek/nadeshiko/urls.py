from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'nadeshiko'

urlpatterns = [
    # Index ex: /nadeshiko/
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('my_account/<int:user_id>', views.my_account, name='my_account'),
    path('quizz/', views.quizz, name='quizz'),
    path('quizz/<int:user_id>', views.quizzesUser, name='quizzesUser'),
    path('hiraganas/', views.hiraganas, name='hiraganas'),
    path('katakanas/', views.katakanas, name='katakanas'),
    path('upload/', views.upload, name='upload'),
    path('loading/', views.loading, name='loading'),
]
