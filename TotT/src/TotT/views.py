from django.views import generic
from django.shortcuts import render

from .forms import WordForm

from .GetGIFs import GetGifInfo

from .bagOfTricks import BagOfTricks

#from .thesaurus import Thesaurus

from os.path import dirname, join

'''
class HomePage(generic.TemplateView):
    template_name = "home.html"

class AboutPage(generic.TemplateView):
    template_name = "about.html"
'''

#t=Thesaurus(join(dirname(__file__),'mthesaur.txt'))
bag=BagOfTricks(mobyPath=join(dirname(__file__),'mthesaur.txt'))

# views added by JRJ to develop further
class SearchPage(generic.TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = {'initForm': 1, 'optRange': range(5,21),}
        return context

    def post(self, request, *args, **kwargs):
        words = WordForm(request.POST)
        if words.is_valid():
            num_word = words.cleaned_data["numWord"]
            bag.setActive(active=words.cleaned_data["urban_bool"], name="urban_dictionary")
            bag.setActive(active=words.cleaned_data["mthe_bool"], name="moby_thesaurus")
            bag.setActive(active=False, name="giffy")
            counter = bag.getCounter(*words.get_list())
            word_list = [x[0].encode('ascii','ignore') for x in counter.most_common(num_word)]
            word_count = [x[1] for x in counter.most_common(num_word)]
            print(word_count)
            conX={'gifs':0, }
            if words.cleaned_data["gif_bool"]==True:
                gif=GetGifInfo()
                q=gif.make_query_simple(words.get_list()[0])
                gif.get_json_object_simple(q)
                imgDat=gif.get_gif_url_original_size_one(0)
                conX['gif']=imgDat
                conX['gifs']=1
                #return render(request, 'search.html', {'gif': imgDat, 'gifs': 1,})
            if words.cleaned_data["mthe_bool"]==True or words.cleaned_data["urban_bool"]==True:
                conX['words']=word_list
                conX['wordCount']=word_count
            return render(request, 'search.html', conX)
        else:
            return render(request, 'search.html', {'error_message': "Please type in some words", 'initForm': 1,  'optRange': range(5,21),})


class ResultsPage(generic.TemplateView):
    template_name = "result.html"
