from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ForumUser)
admin.site.register(Profile)
admin.site.register(ForumPost)
admin.site.register(Reply)
admin.site.register(Vote)