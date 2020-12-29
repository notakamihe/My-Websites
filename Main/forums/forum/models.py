from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpRequest

import datetime

# Create your models here.

class ForumUser (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    dob = models.DateField()
    location = models.CharField(max_length=100, null=True, blank=True)

    @property
    def full_name (self):
        return self.first_name + ' ' + self.surname

    @property
    def dob_month (self):
        months = [
            'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

        return months[self.dob.month - 1]


class Profile (models.Model):
    forum_user = models.OneToOneField(ForumUser, on_delete=models.CASCADE)
    picture = models.ImageField(default='defpfp.jpg', upload_to='profiles/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    @property
    def picture_url (self):
        try:
            return self.picture.url
        except:
            return ''

    @property
    def is_description_whitespace (self):
        return self.description.isspace()

    @property
    def post_count (self):
        return ForumPost.objects.filter(profile=self).count()


class ForumPost (models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=3000, validators=[MinLengthValidator(20)])
    date_posted = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_date_full (self):
        return self.date_posted.strftime('%B %d, %Y')

    @property
    def num_replies (self):
        return Reply.objects.filter(to=self).count()


class Reply (models.Model):
    to = models.ForeignKey(ForumPost, on_delete=models.SET_NULL, null=True)
    replier = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=2000, validators=[MinLengthValidator(10)])
    date_replied = models.DateTimeField(auto_now_add=True)