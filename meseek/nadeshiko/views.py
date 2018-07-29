from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
# Create your views here.

from .models import Hiragana, Katakana
from .level import evaluates
from .quizz import Quizz

QUIZZ_INDEX = {}

def index(request):
    return render(request, 'nadeshiko/index.html')

def quizz(request):
    user = request.user
    username = request.user.username
    try:
        quizz = QUIZZ_INDEX[user.id]
    except KeyError:
        quizz = Quizz(user)
        QUIZZ_INDEX[user.id] = quizz
    finally:
        if request.method == 'POST':
            print("hey i hear you")
            # Retrieves post data
            dataJSON = json.loads(request.body.decode('utf-8'))
            answer = dataJSON['answer']
            print(answer)
            msgServer = {
                "userInfo":
                    {
                    "level": 1,
                    "scores": 0,
                    },
                "quizzIndex": 1,
                "quizzQuestion": quizz.questions[1],
                "quizzLength": 10,
                "reinitConfirmation": False,
                "completion": False,
                "score": 0,
            }
            return JsonResponse(msgServer)
        else:
            return render(request, 'nadeshiko/quizz.html', {'quizz': quizz})

def hiraganas(request):
    hiraganas_list = Hiragana.objects.order_by('id')
    return render(request, 'nadeshiko/hiraganas.html', {'hiraganas': hiraganas_list})

def katakanas(request):
    katakanas_list = Katakana.objects.order_by('id')
    return render(request, 'nadeshiko/katakanas.html', {'katakanas': katakanas_list})

def my_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'nadeshiko/my_account.html', {'user': user})