#! /usr/bin/env python
from ..models import Rappel
from django.shortcuts import get_object_or_404

def remindsMeOf(sentence):
    searchWord = sentence.replace('/r ', '')
    try:
        reminder = Rappel.objects.filter(name=searchWord)[0]
    except IndexError:
    	reminder = None
    else:
        return reminder.rappel


    