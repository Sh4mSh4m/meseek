from django.shortcuts import render

# Create your views here.


def shamnouchi(request):
    return render(request, 'meseek/shamnouchi.html')
