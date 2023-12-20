from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

# Form details for user while creating
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email', 'password1', 'password2','username']
        widgets = {
            'username': forms.HiddenInput(),
            'email': forms.EmailInput(attrs={'onchange':'on_trigger()'}),
        }

    
    