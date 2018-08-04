from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
# Create your views here.

from .models import Hiragana, Katakana
from .level import evaluates
from .quizz import Quizz

QUIZZ_INDEX = {}


#####################
# Support functions #
#####################

def initiatesQuizz(user):
    """
    Support function to return existing quizz or creating one for user
    Quizzes are stored in dict.
    Quizzes are based on Quizz class
    """
    try:
        quizz = QUIZZ_INDEX[user.id]
        if quizz.completed:
            quizz = Quizz(user)
            QUIZZ_INDEX[user.id] = quizz
    except KeyError:
        quizz = Quizz(user)
        QUIZZ_INDEX[user.id] = quizz
    finally:
        return quizz

#####################
#       Views       #
#####################

def index(request):
    """
    Entry view
    """
    return render(request, 'nadeshiko/index.html')

def quizz(request):
    """
    Quizz view handling get and AJAX post requests
    """
    user = request.user
    quizz = initiatesQuizz(user)
    if request.method == 'POST':
        # Retrieves post data
        dataJSON = json.loads(request.body.decode('utf-8'))
        if dataJSON['index'] != 0:
            quizz.updatesData(dataJSON)
        msgServer = {
            "userInfo":
                {
                "level": quizz.level,
                "scores": quizz.scoreSheet,
                },
            "quizzIndex": quizz.index,
            "quizzLength": quizz.size,
            "quizzQuestion": quizz.questions[quizz.index]['jp'],
            "reinitConfirmation": False,
            "completion": quizz.completed,
            "score": quizz.currentScore,
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