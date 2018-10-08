from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Main bot view
def index(request):
    return render(request, 'handmade/index.html')


