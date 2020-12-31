from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseForbidden, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import json
import requests

from forum.forms import *
from .models import *

# Create your views here.
def home_view (request):
    return render(request, 'forum/home.html', {})


def register_view (request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ForumUserForm(request.POST)
        user = CreateUserForm(request.POST)

        if user.is_valid():
            if form.is_valid():
                new_user = user.save()

                new_form = form.save(commit=False)
                new_form.user = new_user
                new_form.save()

                new_profile = Profile(forum_user=new_form)
                new_profile.save()

                login(request, new_user)
                return redirect('profile', forum_user_id=new_form.id)
    else:
        form = ForumUserForm()
        user = CreateUserForm()

    return render(request, 'forum/register.html', {'form': form, 'user': user })


def login_view (request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            forum_user = ForumUser.objects.get(user=user)
            return redirect('profile', forum_user_id=forum_user.id)
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')


    return render(request, 'forum/login.html', {})


def create_view (request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ForumPostForm(request.POST)

        if form.is_valid():
            forum_user = ForumUser.objects.get(user=request.user)
            profile = Profile.objects.get(forum_user=forum_user)

            new_post = form.save(commit=False)
            new_post.profile = profile
            new_post.save()

            return redirect('profile', forum_user_id=forum_user.id)
    else:
        form = ForumPostForm()

    return render(request, 'forum/create.html', { 'form': form })


def profile_details_view (request, forum_user_id):
    if forum_user_id in [obj.id for obj in ForumUser.objects.all()]:
        profile = Profile.objects.get(forum_user=ForumUser.objects.get(id=forum_user_id))
        posts_by_profile = reversed(ForumPost.objects.filter(profile=profile))

        if request.method == 'POST':
            logout(request)
            return redirect('home')
    else:
        raise Http404

    return render(request, 'forum/profile.html', { 
        'profile': profile,
        'is_authorized': request.user == profile.forum_user.user,
        'posts': posts_by_profile
    })


def profile_update_view (request, forum_user_id):
    if forum_user_id in [obj.id for obj in ForumUser.objects.all()]:
        profile = Profile.objects.get(forum_user=ForumUser.objects.get(id=forum_user_id))

        if not request.user.is_superuser:
            if not request.user.is_authenticated or request.user != profile.forum_user.user:
                return HttpResponseForbidden()
        
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

        if not request.user.is_superuser:
            if not request.user.is_authenticated or request.user != profile.forum_user.user:
                return HttpResponseForbidden()

        if request.method == 'POST':
            profile.forum_user.user.delete()
            return redirect('account-deleted')
    else:
        raise Http404

    return render(request, 'forum/profile-delete.html', { 'profile': profile })


def post_list_view (request):
    posts = list(ForumPost.objects.all())[::-1]
    return render(request, 'forum/posts.html', { 'posts': posts })


def post_details_view (request, post_id):
    if post_id in [post.id for post in ForumPost.objects.all()]:
        post = ForumPost.objects.get(id=post_id)
        replies = Reply.objects.filter(to=post)

        if request.method == 'POST':
            reply_form = ReplyFrom(request.POST)

            if request.is_ajax():
                _id = request.POST.get('id')
                reply = Reply.objects.get(id=_id)

                try:
                    content = request.POST.get('reply-content')
                    reply.content = content
                    reply.save()
                except:
                    reply.delete()

                return render(request, 'forum/post_details.html', { 
                    'post': post, 
                    'is_logged_in' : request.user.is_authenticated,
                    'is_authorized': request.user == post.profile.forum_user.user if post.profile else False,
                    'reply_form': reply_form,
                    'replies': replies, 
                    'req_user': request.user
                })


            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.to = post

                forum_user = ForumUser.objects.get(user=request.user)
                profile = Profile.objects.get(forum_user=forum_user)

                reply.replier = profile
                
                reply.save()
                post.save()

            return redirect('post-details', post_id=post.id)
                
            
        else:
            reply_form = ReplyFrom()
        
    else:
        raise Http404

    return render(request, 'forum/post_details.html', { 
        'post': post, 
        'is_logged_in' : request.user.is_authenticated,
        'is_authorized': request.user == post.profile.forum_user.user if post.profile else False,
        'reply_form': reply_form,
        'replies': replies, 
        'req_user': request.user
    })


def post_update_view (request, post_id):
    if post_id in [post.id for post in ForumPost.objects.all()]:
        post = ForumPost.objects.get(id=post_id)

        if not request.user.is_superuser:
            if not request.user.is_authenticated or request.user != post.profile.forum_user.user:
                return HttpResponseForbidden()

        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')

            post.title = title
            post.description = description
            post.save()

            return redirect('post-details', post_id=post.id)
    else:
        raise Http404

    return render(request, 'forum/post-update.html', { 'post': post })


def post_delete_view (request, post_id):
    if post_id in [post.id for post in ForumPost.objects.all()]:
        post = ForumPost.objects.get(id=post_id)

        if not request.user.is_superuser:
            if not request.user.is_authenticated or request.user != post.profile.forum_user.user:
                return HttpResponseForbidden()

        if request.method == 'POST':
            post.delete()
            return redirect('profile', post.profile.forum_user.id)
    else:
        raise Http404

    return render(request, 'forum/post-delete.html', { 'post': post })


def post_vote (request, post_id):
    if post_id in [post.id for post in ForumPost.objects.all()]:
        post = ForumPost.objects.get(id=post_id)

        if request.method == 'POST' and request.user != post.profile.forum_user.user and request.user.is_authenticated:
            is_pos = request.POST.get('is_positive') == 'true'


            if (request.user in [ vote.voter.forum_user.user for vote in Vote.objects.all() ]):
                profile = list(filter(lambda p: p.forum_user.user == request.user, Profile.objects.all()))[0]
                vote = Vote.objects.get(voter=profile)

                if vote.is_positive == is_pos:
                    vote.delete()
                else:
                    vote.is_positive = is_pos
                    vote.save()
            else:
                profile = list(filter(lambda p: p.forum_user.user == request.user, Profile.objects.all()))[0]
                vote = Vote.objects.create(post=post, is_positive=is_pos, voter=profile)
                vote.save()
                
            return JsonResponse({ "standing": post.standing })

            
    else:
        raise Http404

    return JsonResponse({})