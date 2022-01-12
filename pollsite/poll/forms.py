from django import forms
from .models import Choice, Question

class WordForm(forms.Form):
    choice = forms.CharField(label='Add a word', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label='Your username', max_length=100)
    # meeting = forms.CharField(label='Your username', max_length=100)
    meeting_code = forms.CharField(label='The meeting security code', max_length=50)