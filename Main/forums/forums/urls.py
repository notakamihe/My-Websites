"""forums URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from forum.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('create/', create_view, name='create'),
    path('posts/', post_list_view, name='posts'),
    path('posts/<int:post_id>', post_details_view, name='post-details'),
    path('posts/<int:post_id>/update', post_update_view, name='post-update'),
    path('posts/<int:post_id>/delete', post_delete_view, name='post-delete'),
    path('posts/<int:post_id>/vote', post_vote, name='post-vote'),
    path('profiles/<int:forum_user_id>', profile_details_view, name='profile'),
    path('profiles/<int:forum_user_id>/update', profile_update_view, name='profile-update'),
    path('profiles/<int:forum_user_id>/delete', profile_delete_view, name='profile-delete'),
    path('profiles/account-deleted', account_deleted_view, name='account-deleted')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
