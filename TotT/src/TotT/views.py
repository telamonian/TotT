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
    search_type = None
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = None
        if self.search_type=="Gifs":
            context = {
                'gifs': 1,
                }
        else:
            context = {
                'gifs': 0
            }
        return context

    def post(self, request, *args, **kwargs):
        words = WordForm(request.POST)
        if words.is_valid():
            counter = t.getCounter(*words.get_list())
            word_list = [x[0] for x in counter.most_common(5)]
            word_count = [x[1] for x in counter.most_common(5)]
            if self.search_type=="Gifs":
                gif=GetGifInfo()
                q=gif.make_query_complex(word_list)
                gif.get_json_object(q)
                imgDat=gif.get_gif_url_original_size_one(0)
                return render(request, 'search.html', {'gif': imgDat, 'gifs': 1,})
            else:
                return render(request, 'search.html', {'words': word_list, 'gifs': 0, 'wordCount': word_count, })
        else:
            return render(request, 'search.html', {'error_message': "Please type in some words",})


class ResultsPage(generic.TemplateView):
    template_name = "result.html"
