from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
 
from example.forms import *

# Create your views here.
@login_required(login_url='login')
def index (request):
    return render(request, 'example/index.html')

def register (request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'example/register.html', context)

def log_in (request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')
     
    return render(request, 'example/login.html')

def log_out (request):
    logout(request)
    return redirect('login')