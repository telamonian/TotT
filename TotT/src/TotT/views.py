from django.views import generic
from django.shortcuts import render

from .forms import WordForm

from .GetGIFs import GetGifInfo


class HomePage(generic.TemplateView):
    template_name = "home.html"

class AboutPage(generic.TemplateView):
    template_name = "about.html"

# views added by JRJ to develop further
class SearchPage(generic.TemplateView):
    template_name = "search.html"

    '''def form_valid(self, form):
        return render(request, 'search.html', {'words': form.sub_words,})'''
    def post(self, request, *args, **kwargs):
        words = WordForm(request.POST)
        if words.is_valid():
            gif=GetGifInfo()
            q=gif.make_query_simple(words.get_list()[0])
            gif.get_json_object(q)
            imgDat=gif.get_gif_url_original_size_one(0)
            return render(request, 'search.html', {'gif': imgDat,})
        else:
            return render(request, 'search.html', {'error_message': "Please type in some words",})
'''
        #if(request.POST.get('search_thesaurus')):
            some_val = 'did it stick? {0}'.format(request.GET.get('search_words'))
            return HttpResponse('results')
        else:
            return HttpResponse('search')'''

class ResultsPage(generic.TemplateView):
    template_name = "result.html"
