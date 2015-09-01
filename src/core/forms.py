from django.contrib.auth.models import User
from django import forms

from core.models import Round

class UserForm(forms.ModelForm):
    password = forms.CharField(label="Passwort", widget=forms.PasswordInput())
    password_repeat = forms.CharField(label="Passwort wiederholen", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'password_repeat')


class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ('pkt1', 'pkt2')
