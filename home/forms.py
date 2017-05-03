from django import forms
from home.models import comment
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class comment_form(forms.ModelForm):
    text = forms.CharField(required=False,widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control',
                                      'placeholder': 'Write a Comment..'
                                  }
                                  ))
    class Meta:
        model=comment
        fields= ('text',)
