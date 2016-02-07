from django.views import generic
from django.shortcuts import render

from .forms import WordForm

from .GetGIFs import GetGifInfo

from .thesaurus import Thesaurus

from os.path import dirname, join

'''
class HomePage(generic.TemplateView):
    template_name = "home.html"

class AboutPage(generic.TemplateView):
    template_name = "about.html"
'''

t=Thesaurus(join(dirname(__file__),'mthesaur.txt'))

# views added by JRJ to develop further
class SearchPage(generic.TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = {'initForm': 1,}
        return context

    def post(self, request, *args, **kwargs):
        words = WordForm(request.POST)
        if words.is_valid():
            counter = t.getCounter(*words.get_list())
            word_list = [x[0] for x in counter.most_common(20)]
            word_count = [x[1] for x in counter.most_common(20)]
            conX={'gifs':0, }
            if words.cleaned_data["gif_bool"]==True:
                gif=GetGifInfo()
                q=gif.make_query_complex(words.get_list()[0])
                gif.get_json_object(q)
                imgDat=gif.get_gif_url_original_size_one(0)
                conX['gif']=imgDat
                conX['gifs']=1
                #return render(request, 'search.html', {'gif': imgDat, 'gifs': 1,})
            if words.cleaned_data["mthe_bool"]==True:
                conX['words']=word_list
                conX['wordCount']=word_count
            return render(request, 'search.html', conX)
        else:
            return render(request, 'search.html', {'error_message': "Please type in some words", 'initForm': 1, })


class ResultsPage(generic.TemplateView):
    template_name = "result.html"
