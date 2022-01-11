from django import forms

class WordForm(forms.Form):
    choice = forms.CharField(label='Add a word', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label='Your username', max_length=100)
    # meeting = forms.CharField(label='Your username', max_length=100)