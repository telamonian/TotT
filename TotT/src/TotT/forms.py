from django import forms

class WordForm(forms.Form):
    sub_words = forms.CharField(label= "Words",max_length=1000)
