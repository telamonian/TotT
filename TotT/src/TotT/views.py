from django.views import generic
from django.shortcuts import render

from .forms import WordForm

from .GetGIFs import GetGifInfo

'''
class HomePage(generic.TemplateView):
    template_name = "home.html"

class AboutPage(generic.TemplateView):
    template_name = "about.html"
'''
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
            if self.search_type=="Gifs":
                gif=GetGifInfo()
                q=gif.make_query_simple(words.get_list()[0])
                gif.get_json_object(q)
                imgDat=gif.get_gif_url_original_size_one(0)
                return render(request, 'search.html', {'gif': imgDat, 'gifs': 1,})
            else:
                return render(request, 'search.html', {'words': words.get_list(), 'gifs': 0,})
        else:
            return render(request, 'search.html', {'error_message': "Please type in some words",})


class ResultsPage(generic.TemplateView):
    template_name = "result.html"
