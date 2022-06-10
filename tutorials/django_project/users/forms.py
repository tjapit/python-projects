from dataclasses import field, fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """ New form class that inherits from UserCreationForm provided from Django """
    # added email field to the form
    email = forms.EmailField() # required default true

    class Meta:
        """ Gives us a nested namespace for configuration, and keeps the configurations in one place """
        # saves the form as a User model
        model = User
        # fields that we want in the form and in the order we want
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
