from django import forms

class WordForm(forms.Form):
    sub_words = forms.CharField(label= "Words",max_length=1000)

    def get_list(self):
        s=self.cleaned_data['sub_words']
        l=s.replace(","," ").split()
        return l
