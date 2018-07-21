from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

# For login and signup
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

def shamnouchi(request):
    return render(request, 'meseek/shamnouchi.html')


def my_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'meseek/my_account.html', {'user': user})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('shamnouchi')
    else:
        form = SignUpForm()
    return render(request, 'meseek/signup.html', {'form': form})