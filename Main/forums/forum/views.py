from django.shortcuts import render, redirect
from django.http import Http404

import json
import requests

from forum.forms import *
from .models import *

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

            new_user = User(username=username.lower(), password=password)
            new_user.save()

            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = new_user
                new_form.save()

                new_profile = Profile(forum_user=new_form)
                new_profile.save()

                return redirect('profile', forum_user_id=new_form.id)
    else:
        form = ForumUserForm()
        user = CreateUserForm()

    return render(request, 'forum/register.html', {'form': form, 'user': user })


def login_view (request):
    return render(request, 'forum/login.html', {})


def create_view (request):
    return render(request, 'forum/create.html', {})


def profile_details_view (request, forum_user_id):
    if forum_user_id in [obj.id for obj in ForumUser.objects.all()]:
        profile = Profile.objects.get(forum_user=ForumUser.objects.get(id=forum_user_id))
    else:
        raise Http404

    return render(request, 'forum/profile.html', { 'profile': profile })


def profile_update_view (request, forum_user_id):
    if forum_user_id in [obj.id for obj in ForumUser.objects.all()]:
        profile = Profile.objects.get(forum_user=ForumUser.objects.get(id=forum_user_id))

        if request.method == 'POST':
            if (request.FILES):
                profile.picture = request.FILES['profile-img-input']
                profile.save()
            else:
                first_name = request.POST.get('first_name')
                surname = request.POST.get('surname')
                description = request.POST.get('description')
                dob = datetime.datetime.strptime(request.POST.get('dob'), '%Y-%m-%d')
                location = request.POST.get('location')

                profile.description = description
                profile.forum_user.first_name = first_name
                profile.forum_user.surname = surname
                profile.forum_user.dob = dob
                profile.forum_user.location = location
                profile.save()
                profile.forum_user.save()

                return redirect('profile', forum_user_id=forum_user_id)

    else:
        raise Http404

    return render(request, 'forum/profile-update.html', { 'profile': profile })


def account_deleted_view (request):
    return render(request, 'forum/account-deleted.html', {})


def profile_delete_view (request, forum_user_id):
    if forum_user_id in [obj.id for obj in ForumUser.objects.all()]:
        profile = Profile.objects.get(forum_user=ForumUser.objects.get(id=forum_user_id))

        if request.method == 'POST':
            profile.forum_user.user.delete()
            return redirect('account-deleted')
    else:
        raise Http404

    return render(request, 'forum/profile-delete.html', { 'profile': profile })


def post_list_view (request):
    return render(request, 'forum/posts.html', {})


def post_details_view (request):
    return render(request, 'forum/post_details.html', {})