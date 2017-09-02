from django import forms
from home.models import comment
from account.models import compare_comment
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class comment_form(forms.ModelForm):
    class Meta:
        model=comment
        fields= ['text']
        widgets = {
            'text': forms.TextInput(
                attrs={'class':'comment_box','id': 'post-comment', 'required': True, 'placeholder': 'Write a comment...'}
            ),
        }


class compare_comment_form(forms.ModelForm):
    class Meta:
        model=compare_comment
        fields= ['text']
        widgets = {
            'text': forms.TextInput(
                attrs={'class':'comment_box','id': 'post-comment', 'required': True, 'placeholder': 'Write a comment...'}
            ),
        }
