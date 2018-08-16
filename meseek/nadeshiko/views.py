import json
import pytesseract
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from PIL import Image, ImageFilter
# Create your views here.
from .models import Hiragana, Katakana
from .quizz import Quizz, QuizzConfigurationForm, OCRTextForm


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

def ocr(filename):
    """
    Opens file and applies OCR on it to get both japanese and english
    """
    img = Image.open(filename)
    img.filter(ImageFilter.SHARPEN)
    text = pytesseract.image_to_string(img, config="-psm 6", lang="jpn+eng")
    return text.split('\n')

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
    View handling configuring or resuming the quizz
    """
    user = request.user
    quizz = initiatesQuizz(user)
    # form generating with default value
    form = QuizzConfigurationForm({'Difficulté':10})
    # Checking form conformity
    if request.method == 'POST':
        # Creates another form instance with post data
        form = QuizzConfigurationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['Difficulté'] != quizz.size:
                quizz.size = int(form.cleaned_data['Difficulté'])
                quizz.questions = quizz.populatesQuestions()
                quizz.answers = quizz.populatesAnswers()
                quizz.index = quizz.currentIndex()
            # redirection if form is valid
            return HttpResponseRedirect('{}'.format(user.id))
    else:
        return render(request, 'nadeshiko/quizz.html', {'quizz': quizz, 'form': form})

def quizzesUser(request, user_id):
    """
    View dedicated to the users quizz
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
            "lastAnswer": quizz.lastAnswer,
            "reinitConfirmation": False,
            "completion": quizz.completed,
            "score": quizz.currentScore,
        }
        return JsonResponse(msgServer)
    first_question = quizz.questions[quizz.index]['jp']
    return render(request, 'nadeshiko/quizz_user.html', {'quizz': quizz, 'first_question': first_question})


def hiraganas(request):
    hiraganas_list = Hiragana.objects.order_by('id')
    return render(request, 'nadeshiko/hiraganas.html', {'hiraganas': hiraganas_list})

def katakanas(request):
    katakanas_list = Katakana.objects.order_by('id')
    return render(request, 'nadeshiko/katakanas.html', {'katakanas': katakanas_list})

def my_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'nadeshiko/my_account.html', {'user': user})

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        path2file = "." + uploaded_file_url
        wordList = ocr(path2file)
        rows = len(wordList)
        form = OCRTextForm(wordList)
        print("successfully crearted form")
        print(form)
        return render(request, 'nadeshiko/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url, 'wordList': wordList, 'rows': rows, 'form': form })
    return render(request, 'nadeshiko/simple_upload.html')


def loading(request):
    if request.method == 'POST':
        print("alright got it")
        dataJSON = json.loads(request.body.decode('utf-8'))
        print(dataJSON)
        return JsonResponse({"response": "ok"})