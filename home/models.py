from __future__ import unicode_literals
import datetime
from django.utils.encoding import smart_unicode
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#model for comments


#class likes

#class suggestions


#
class Post(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    source=models.CharField(max_length=1000,default="Anonymous")
    author=models.CharField(max_length=1000,default="Anonymous")
    headline=models.TextField(max_length=1000,default="")
    story=models.TextField(max_length=10000,default="")
    link = models.URLField("Photo Link",blank=True, max_length=1000, help_text="The URL to the image page")
    image=models.ImageField(upload_to="Newspictures",blank=True,default='profile_pictures/Dp.png')
    date=models.DateField(default=timezone.now)
    pageurl=models.URLField("Pagelink",blank=True,max_length=1000,help_text="The URL to newspage")
    likes=models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)
    suggestions=models.IntegerField(default=0)
    visits=models.PositiveIntegerField(default=0)
    totalcomments=models.IntegerField(default=0)
    comments=models.ManyToManyField('comment',related_name='comments_to_post')

    def __unicode__(self):
        return smart_unicode(self.headline)

    class Meta:
        unique_together=("headline","author")

class Likes(models.Model):
    post = models.ForeignKey(Post, related_name='likedpost')
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return smart_unicode(self.post.headline)

    @classmethod
    def like(cls,postid,liker):
        lik,created=cls.objects.get_or_create(
            post=postid
          )
        lik.users.add(liker)

    @classmethod
    def unlike(cls,postid,unliker):
        unlik,created=cls.objects.get_or_create(post=postid)
        unlik.users.remove(unliker)

class Dislikes(models.Model):
    post=models.ForeignKey(Post,related_name='dislikedpost')
    users=models.ManyToManyField(User)

    def __unicode__(self):
        return smart_unicode(self.post.headline)

    @classmethod
    def dislike(cls,postid,disliker):
        dislik,created=cls.objects.get_or_create(
            post=postid
          )
        dislik.users.add(disliker)

    @classmethod
    def undislike(cls,postid,undisliker):
        undislik,created=cls.objects.get_or_create(
            post=postid
          )
        undislik.users.remove(undisliker)


class comment(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)    #when comment was created first
    updated_on = models.DateTimeField(auto_now=True)    #if edited else equal to created_on value
    user=models.ForeignKey(User)    #user who made the comment
    text=models.TextField(max_length=1000,blank=False)    #text of the comment max_length 1000 handle error for max length
    likes=models.IntegerField(default=0)    #total number of likes on that commemt
        #no dislike for comments
    post=models.ForeignKey(Post,related_name='postlink')    #post id to which the comment belongs
    reply=models.ManyToManyField('comment')    #comment id to whom this comment is reply to else value remains zero

    def __unicode__(self):
        return self.text+' - '+self.user.username    #to show username in admin interface

    class Meta:
        unique_together=("user","text")
