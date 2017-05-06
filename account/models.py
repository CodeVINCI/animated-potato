from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.forms import ModelForm

# Create your models here.

class Userprofile(models.Model):

    #user=models.ForeignKey(User)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workAndemployment=models.CharField(max_length=200,default='',blank=True)
    location=models.CharField(max_length=100,default='',blank=True)
    website=models.URLField(default='',blank=True)
    description=models.TextField(max_length=300,default='',blank=True)
    image=models.ImageField(upload_to='profile_pictures',blank=True,default='profile_pictures/Dp.png')


    def __str__(self):
        return self.user.username




class SocratesSearch(models.Model):
    user=models.ForeignKey(User)
    search=models.CharField(max_length=200,default='',blank=False)
    searchdate=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Following(models.Model):
    users=models.ManyToManyField(User,related_name='people')
    current_user=models.ForeignKey(User, related_name='owner', null=True)

    def __str__(self):
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


