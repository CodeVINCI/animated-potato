from django import forms
from account.models import Userprofile,SocratesSearch
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.files.images import get_image_dimensions

from django import forms

class UserProfile_form(forms.ModelForm):
    workAndemployment = forms.CharField(max_length=200,required=False,
                                        widget=forms.TextInput(
                                            attrs={
                                                'class':'form-control',
                                                'placeholder': 'Add Work And Employment..'
                                            }
                                        ))
    location = forms.CharField(label='location',max_length=100,required=False,

                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Add a Location..'
                                   }
                               ))
    website = forms.URLField(required=False,
                            widget = forms.URLInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Add Your Website..'
                                 }
                            ))


    description = forms.CharField(required=False,widget=forms.Textarea(
                                  attrs={
                                      'class': 'form-control',
                                      'placeholder': 'Write a Description..'
                                  }
                                  ))
    class Meta:
        model=Userprofile
        fields= ('workAndemployment','location','website','description',)


class Upload_form(forms.ModelForm):
    image=forms.ImageField(required=False)

    class Meta:
        model=Userprofile
        fields=('image',)

    def clean_avatar(self):
        image = self.cleaned_data['image']

        try:
            w, h = get_image_dimensions(image)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(image) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return image


class SocratesSearchForm(forms.ModelForm):
    search=forms.CharField(max_length=200,required=False,
                                        widget=forms.TextInput(
                                            attrs={
                                                'class':'form-control',
                                                'placeholder': 'Search-Socrates'
                                            }
                                        ))
    class Meta:
        model=SocratesSearch
        fields=('search',)
