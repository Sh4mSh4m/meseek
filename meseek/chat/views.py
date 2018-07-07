import time
import json
import re
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from chat.authhelper import get_signin_url, get_token_from_code, get_access_token
from chat.outlookservice import get_me, get_my_messages
from .f_parser.parser import msgParser
from .f_parser.questionsProc import questionsProc
from .f_parser.requestsAPI import getJsonApiWiki
from .f_chatterbot.chatterbot import Meseek
from .f_reminders.remindsMeOf import remindsMeOf

# Initiating chatbots dict, key being userIds
# After django app, chatbots are reinitialized
# Further addons will save bots data into db
chatbots = {}

# Main bot view
def index(request):
    if request.method == 'POST':
        # Retrieves post data
        dataJSON = json.loads(request.body.decode('utf-8'))
        userId = int(dataJSON['userId'])
        rawMat = dataJSON['rawInput']
        msgResponse = {'interaction': "",
                   'complement': "",
                   'keyWord': "",
                   'response': "",
                   'list': ""}
        parsedBatch = msgParser(rawMat)
        lstSentences = parsedBatch['sentences']
        lstQuestions = parsedBatch['questions']
        # Processes questions
        if len(lstQuestions) != 0:
            msgResponse = questionsProc(lstQuestions, msgResponse)
            if msgResponse['keyWord'] != '':
                msgResponse['response'] = getJsonApiWiki(msgResponse['keyWord'])
                if msgResponse['response'] != '':
                    msgResponse['complement'] = "D'ailleurs, savais-tu que "
                    msgResponse['complement'] += msgResponse['response']
            else:
                msgResponse['complement'] = "Désolé je n'ai rien trouvé"
        # Processes sentences
        if userId not in chatbots.keys():
            chatbots[userId] = Meseek(userId)
        for sentence in lstSentences:
            if re.match(r"^/r \S", str(sentence)):
                match = remindsMeOf(sentence)
                if match == None:
                    msgResponse['interaction'] += "Désolé pas de commande correspondante"
                else:
                    msgResponse['list'] += match
            else:    
                msgResponse['interaction'] += str(chatbots[userId].get_response(sentence))
        return JsonResponse(msgResponse)
    elif request.method == 'GET':
        return render(request, 'chat/index.html')


# OUTLOOK API views
def home(request):
    redirect_uri = request.build_absolute_uri(reverse('chat:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')
    #return render(request, 'chat/home.html', {'sign_in_url': sign_in_url })

def gettoken(request):  
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('chat:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    user = get_me(access_token)
    refresh_token = token['refresh_token']
    expires_in = token['expires_in']
    # expires_in is in seconds
    # Get current timestamp (seconds since Unix Epoch) and
    # add expires_in to get expiration time
    # Subtract 5 minutes to allow for clock differences
    expiration = int(time.time()) + expires_in - 300
    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token
    request.session['token_expires'] = expiration
    return HttpResponseRedirect(reverse('chat:mail'))

def mail(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('chat:gettoken')))
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('chat:home'))
    else:
        messages = get_my_messages(access_token)
        context = { 'messages': messages['value'] }
        return render(request, 'chat/mail.html', context)
