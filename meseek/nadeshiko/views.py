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
        print("Voilà le lot de questions: {}".format(quizz.questions))
        if request.method == 'POST':
            # Retrieves post data
            dataJSON = json.loads(request.body.decode('utf-8'))
            answer = dataJSON['answer']
            answerIndex = dataJSON['index']
            quizz.answers[answerIndex] = answer
            quizz.index = quizz.currentIndex()
            print("Current index is {}".format(quizz.index))
            print("Tes réponses sont {}".format(quizz.answers))
            msgServer = {
                "userInfo":
                    {
                    "level": quizz.level,
                    "scores": quizz.scoreSheet,
                    },
                "quizzIndex": quizz.index,
                "quizzQuestion": quizz.questions[quizz.index]['jp'],
                "quizzLength": quizz.size,
                "reinitConfirmation": False,
                "completion": False,
                "score": 0,
            }
            print(msgServer)
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