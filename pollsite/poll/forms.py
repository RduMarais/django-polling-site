from django import forms

class WordForm(forms.Form):
    choice = forms.CharField(label='Add a word', max_length=100)
