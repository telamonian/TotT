from django import forms

class WordForm(forms.Form):
    sub_words = forms.CharField(label= "Words",max_length=1000)
    urban_bool = forms.BooleanField(initial=False, label= "Urban", required=False)
    mthe_bool = forms.BooleanField(initial=True, label= "MThesaur", required=False)
    gif_bool = forms.BooleanField(initial=False, label= "Giphy", required=False)
    numWord = forms.IntegerField(label= "numWord")

    def get_list(self):
        s=self.cleaned_data['sub_words']
        l=s.replace(","," ").split()
        return l
