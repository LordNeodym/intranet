from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(label="Passwort", widget=forms.PasswordInput())
    password_repeat = forms.CharField(label="Passwort wiederholen", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'password_repeat')
