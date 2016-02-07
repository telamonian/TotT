from django.views import generic
from django.shortcuts import render

from .forms import WordForm

from .GetGIFs import GetGifInfo

from .thesaurus import Thesaurus

#import os

'''
class HomePage(generic.TemplateView):
    template_name = "home.html"

class AboutPage(generic.TemplateView):
    template_name = "about.html"
'''
#print(os.listdir("."))
t=Thesaurus('TotT/mthesaur.txt')

# views added by JRJ to develop further
class SearchPage(generic.TemplateView):
    template_name = "search.html"

    def post(self, request, *args, **kwargs):
        words = WordForm(request.POST)
        if words.is_valid():
            counter = t.getCounter(*words.get_list())
            l=[]
            for i in counter.most_common(2):
                l.append(i[0])
            print(l)
            conX={'gifs':0,}
            if words.cleaned_data["gif_bool"]==True:
                gif=GetGifInfo()
                q=gif.make_query_complex(words.get_list()[0])
                gif.get_json_object(q)
                imgDat=gif.get_gif_url_original_size_one(0)
                conX['gif']=imgDat
                conX['gifs']=1
                #return render(request, 'search.html', {'gif': imgDat, 'gifs': 1,})
            if words.cleaned_data["mthe_bool"]==True:
                conX['words']=l
            return render(request, 'search.html', conX)
        else:
            return render(request, 'search.html', {'error_message': "Please type in some words",})


class ResultsPage(generic.TemplateView):
    template_name = "result.html"
