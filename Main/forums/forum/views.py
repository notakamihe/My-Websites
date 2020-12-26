from django.shortcuts import render, redirect
from forum.forms import *

# Create your views here.
def home_view (request):
    return render(request, 'forum/home.html', {})


def register_view (request):
    if request.method == 'POST':
        form = ForumUserForm(request.POST)
        user = CreateUserForm(request.POST)

        if user.is_valid():
            username = user.cleaned_data.get('username')
            password = user.cleaned_data.get('password1')

            new_user = User(username=username, password=password)
            new_user.save()

            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = new_user
                new_form.save()

                return redirect('home')
    else:
        form = ForumUserForm()
        user = CreateUserForm()

    return render(request, 'forum/register.html', {'form': form, 'user': user })


def login_view (request):
    return render(request, 'forum/login.html', {})


def create_view (request):
    return render(request, 'forum/create.html', {})


def post_list_view (request):
    return render(request, 'forum/posts.html', {})


def post_details_view (request):
    return render(request, 'forum/post_details.html', {})