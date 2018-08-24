import json
import pytesseract
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from PIL import Image, ImageFilter
# Create your views here.
from .models import Hiragana, Katakana, LessonScan, Vocabulary
from .forms import QuizzConfigurationForm, OCRTextForm, LessonScanForm
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

def ocr(filename):
    """
    Opens file and applies OCR on it to get both japanese and english
    """
    img = Image.open(filename)
    img.filter(ImageFilter.SHARPEN)
    text = pytesseract.image_to_string(img, config="-psm 6", lang="jpn+fra")
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
    """
    Simple Hiraganas view
    """
    hiraganas_list = Hiragana.objects.order_by('id')
    return render(request, 'nadeshiko/hiraganas.html', {'hiraganas': hiraganas_list})

def katakanas(request):
    """
    Simple Kakatanas view
    """
    katakanas_list = Katakana.objects.order_by('id')
    return render(request, 'nadeshiko/katakanas.html', {'katakanas': katakanas_list})

def my_account(request, user_id):
    """
    Simple account information view
    """
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'nadeshiko/my_account.html', {'user': user})

def upload(request):
    """
    Uploads file, processes through OCR function and returns dynamic form with content of OCR text
    """
    wordList = []
    if request.method == 'POST' and 'image' in request.FILES.keys():
        form = LessonScanForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save()
            # stupid way to collect
            path2file = "." + "/media/" + str(scan.image)
            wordList = ocr(path2file) 
            rows = len(wordList)
            formToEdit = OCRTextForm(initial={'Type':'vocabulaire'}, wordList=wordList)  # dynamic form creation
            return render(request, 'nadeshiko/simple_upload.html', {
            'scan': scan, 'wordList': wordList, 'rows': rows, 'formToEdit': formToEdit })
    elif request.method == 'POST':
        formToEdit = OCRTextForm(request.POST, wordList=wordList)
        if formToEdit.is_valid():
            voc_type = formToEdit.cleaned_data['Type'] 
            level = formToEdit.cleaned_data['Level'] 
            for key, value in request.POST.items():
                if "Mot" in key and value != '':
                    word=Vocabulary(voc_jp=value.split('//')[0])
                    word.voc_fr = value.split('//')[1]
                    word.level=level
                    word.voc_type=voc_type
                    word.save()
            return JsonResponse({'message':"ok"})
    else:
        form = LessonScanForm()
        return render(request, 'nadeshiko/simple_upload.html', {'form': form})


def loading(request):
    if request.method == 'POST':
        form = OCRTextForm()
        if form.is_valid():
            print(form.__dict__)
            return JsonResponse({'message':"ok"})
