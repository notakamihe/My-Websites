from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

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
        

class Profile (models.Model):
    forum_user = models.OneToOneField(ForumUser, on_delete=models.CASCADE)
    picture = models.ImageField(default='defpfp.jpg', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, null=True, blank=True)


class ForumPost (models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=3000, validators=[MinLengthValidator(20)])
    date_posted = models.DateTimeField(auto_now_add=True)
    comments = models.IntegerField(default=0, null=True, blank=True)
    upvotes = models.IntegerField(default=0, null=True, blank=True)