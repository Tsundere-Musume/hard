from django import forms
from django.contrib.auth.models import User
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm

THEME_CHOICES = [
    ('dark', 'dark'),
    ('light', 'light'),
]

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() # Required
    theme = forms.ChoiceField(required = True, choices = THEME_CHOICES, widget=forms.RadioSelect(attrs={'class' : 'Radio'}), initial='dark')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'theme']

class UserSigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Updating Profile
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField() # Required
    # oldpass = forms.CharField(widget=forms.PasswordInput)
    # newpass1 = forms.CharField(widget=forms.PasswordInput)
    # newpass2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']


class MyUserUpdateForm(forms.ModelForm):
    theme = forms.ChoiceField(required = True, choices = THEME_CHOICES, widget=forms.RadioSelect(attrs={'class' : 'Radio'}), initial='dark')
    class Meta:
        model = MyUser
        fields = ['image', 'banner', 'theme']