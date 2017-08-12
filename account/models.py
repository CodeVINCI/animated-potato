from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import ModelForm
from home.models import Post
from django.core.exceptions import ValidationError

# Create your models here.

class Userprofile(models.Model):

    user=models.ForeignKey(User)
    workAndemployment=models.CharField(max_length=200,default='',blank=True)
    location=models.CharField(max_length=100,default='',blank=True)
    website=models.URLField(default='',blank=True)
    description=models.TextField(max_length=300,default='',blank=True)
    image=models.ImageField(upload_to='profile_pictures',blank=True,default='profile_pictures/Dp.png')


    def __str__(self):
        return self.user.username

class newspaper(models.Model):
    name= models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering=('name',)



class SocratesSearch(models.Model):
    user=models.ForeignKey(User)
    search=models.CharField(max_length=200,default='',blank=False)
    searchdate=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username


class Following(models.Model):
    users=models.ManyToManyField(User,related_name='people')
    newspaper=models.ManyToManyField(newspaper)
    post=models.ManyToManyField(Post)
    current_user=models.ForeignKey(User, related_name='owner',null=True)

    def __unicode__(self):
        return str(self.current_user)

    @classmethod
    def followfriend(cls, current_user, new_following):
        follower,created=cls.objects.get_or_create(
            current_user=current_user
        )
        follower.users.add(new_following)

    @classmethod
    def unfollowfriend(cls, current_user, new_following):
        follower,created=cls.objects.get_or_create(
            current_user=current_user
        )
        follower.users.remove(new_following)

    @classmethod
    def Subscribenews(cls,current_user,new_newspaper):
        follower,created=cls.objects.get_or_create(
            current_user=current_user
        )
        follower.newspaper.add(new_newspaper)

    @classmethod
    def Unsubscribenews(cls,current_user,new_newspaper):
        follower,created=cls.objects.get_or_create(
            current_user=current_user
        )
        follower.newspaper.remove(new_newspaper)

    @classmethod
    def addpost(cls,current_user,post):
        follower,created=cls.objects.get_or_create(
            current_user=current_user
        )
        follower.post.add(post)

    @classmethod
    def removepost(cls,current_user,post):
        follower,created=cls.objects.get_or_create(
            current_user=current_user
        )
        follower.post.remove(post)

class Notification(models.Model):
    user=models.ForeignKey(User)
    message=models.CharField(max_length=1000)
    onclick_url=models.URLField(blank=True)
    seen=models.BooleanField(default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    seen_on=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

class Compare(models.Model):
    created_on=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User)
    title=models.CharField(max_length=500,default="")
    description=models.CharField(max_length=10000,default="")
    posts=models.ManyToManyField(Post)
    published=models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

class compare_comment(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)    #when comment was created first
    updated_on = models.DateTimeField(auto_now=True)    #if edited else equal to created_on value
    user=models.ForeignKey(User)    #user who made the comment
    text=models.TextField(max_length=1000,blank=False)    #text of the comment max_length 1000 handle error for max length
    likes=models.IntegerField(default=0)    #total number of likes on that commemt
        #no dislike for comments
    post=models.ForeignKey(Compare,related_name='comparelink')    #post id to which the comment belongs
    reply=models.ManyToManyField('compare_comment')    #comment id to whom this comment is reply to else value remains zero

    def __unicode__(self):
        return self.text+' - '+self.user.username    #to show username in admin interface

    class Meta:
        unique_together=("user","text","created_on")
