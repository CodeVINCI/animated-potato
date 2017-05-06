from __future__ import unicode_literals
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class SignUp_form(UserCreationForm):
    email=forms.EmailField(required='True',
                        widget = forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Email Address'
        }
                           ))
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput())

        model = User
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control1',
                                                'placeholder': 'First name',

                                                 }),
            'last_name': forms.TextInput(attrs={'class': 'form-control2',
                                                 'placeholder': 'Surname',

                                                 }),
            'password': forms.PasswordInput(attrs={'class': 'form-control4',
                                                   'placeholder': 'Password',

            }),
            'username': forms.TextInput(attrs={'class': 'form-control3',
                                                    'placeholder': 'Username'

                                                    }),

        }
        fields={'first_name',
                'last_name',
                'email',
                'password',
                'username',
                }
    def save(self,commit=True):
        user=super(SignUp_form,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email= self.cleaned_data['email']
        if commit:
            user.save()
        return user



class UserBasicEdit_form(UserChangeForm):
    class Meta:
        model=User
        fields=('first_name',
                'last_name',
        )

