from __future__ import unicode_literals
import datetime
from django.utils.encoding import smart_unicode

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#model for comments

class comment(models.Model):
    created_on = models.DateTimeField(default=timezone.now)    #when comment was created first
    updated_on = models.DateTimeField(default=timezone.now)    #if edited else equal to created_on value
    user=models.OneToOneField(User)    #user who made the comment
    text=models.TextField(max_length=1000,default="",blank=True)    #text of the comment max_length 1000 handle error for max length
    likes=models.IntegerField(default=0)    #total number of likes on that commemt
        #no dislike for comments
    post=models.IntegerField()    #post id to which the comment belongs
    replyto=models.IntegerField(default=0)    #comment id to whom this comment is reply to else value remains zero

    def __str__(self):
        return self.user.username    #to show username in admin interface

#class likes

#class suggestions


#
class Post(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    source=models.CharField(max_length=100,default="Anonymous")
    author=models.CharField(max_length=100,default="Anonymous")
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

