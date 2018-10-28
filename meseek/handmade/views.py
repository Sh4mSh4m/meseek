from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import UserWeeklyBasketScore

def index(request):
    current_score = UserWeeklyBasketScore.objects.order_by('-score_ratio')
    winner = current_score[0]
    context = {'winner': winner,
    'current_score': current_score}
    return render(request, 'handmade/index.html', context)


def referee(request):
    current_score = UserWeeklyBasketScore.objects.order_by('-score_ratio')
    winner = current_score[0]
    context = {'winner': winner,
    'current_score': current_score}
    return render(request, 'handmade/referee.html', context)
