from __future__ import unicode_literals
import datetime
from django.utils.encoding import smart_unicode

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class comment(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    user=models.OneToOneField(User)
    text=models.TextField(max_length=200,default="",blank=True)
    likes=models.IntegerField(default=0)
    post=models.IntegerField()
    replyto=models.IntegerField(default=0)

    def __str__(self):
        return self.user.username



class Post(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    source=models.CharField(max_length=50,default="Anonymous")
    author=models.CharField(max_length=25,default="Anonymous")
    headline=models.TextField(max_length=1000,default="")
    story=models.TextField(max_length=10000,default="")
    link = models.URLField("Photo Link",blank=True, max_length=255, help_text="The URL to the image page")
    image=models.ImageField(upload_to="Newspictures",blank=True,default='profile_pictures/Dp.png')
    date=models.DateField(default=timezone.now)
    pageurl=models.URLField("Pagelink",blank=True,max_length=500,help_text="The URL to newspage")
    likes=models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)
    suggestions=models.IntegerField(default=0)
    totalcomments=models.IntegerField(default=0)
    comment=models.IntegerField(default=0)

    def __unicode__(self):
        return smart_unicode(self.headline)

