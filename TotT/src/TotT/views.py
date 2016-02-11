from django.views import generic
from django.shortcuts import render
import numpy as np
from os.path import dirname, join
import random

from .bagOfTricks import BagOfTricks
from .forms import WordForm
from .GetGIFs import GetGifInfo

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
            '''bag.setActive(active=words.cleaned_data["urban_bool"], name="urban_dictionary")
            bag.setActive(active=words.cleaned_data["mthe_bool"], name="moby_thesaurus")
            bag.setActive(active=False, name="giffy")'''
            activeList=[]
            if words.cleaned_data["urban_bool"]:
                activeList.append("urban_dictionary")
            if words.cleaned_data["mthe_bool"]:
                activeList.append("moby_thesaurus")
            counter = bag.getCounter(*words.get_list(), active=activeList)
            word_list = [x[0].encode('ascii','ignore') for x in counter.most_common(num_word)]
            word_count = [x[1] for x in counter.most_common(num_word)]
            if words.cleaned_data["urban_bool"]==False and words.cleaned_data["mthe_bool"]==False:
                word_list=words.get_list()
                word_list.append("")
            print(word_count)
            conX={'gifs':0, 'oldWords':", ".join(words.get_list()),}
            if words.cleaned_data["gif_bool"]==True and len(word_list)>=3:
                gif=GetGifInfo()
                print(word_list[0:3])
                q=gif.make_query_complex(word_list[0:3])
                gif.get_json_object_complex(q)
                imgDat=gif.get_gif_url_original_size_all()
                if len(imgDat)<5:
                    gif2=GetGifInfo()
                    q2=gif2.make_query_complex(words.get_list())
                    gif2.make_query_complex(q2)
                    imgDat=gif2.get_gif_url_original_size_all()
                if len(imgDat)==0:
                    conX['error_message']= "No Gifs"
                else:
                    imgDat=random.choice(imgDat)
                    conX['gif']=imgDat
                    conX['gifs']=1
                #return render(request, 'search.html', {'gif': imgDat, 'gifs': 1,})
            if (words.cleaned_data["mthe_bool"]==True or words.cleaned_data["urban_bool"]==True) and len(word_list)!=0:
                conX['words']=word_list
                conX['newWords']=", ".join(word_list)
                conX['wordCount']=word_count
                conX['wordCountMax']=np.max(word_count)
                conX['wordCountMin']=np.min(word_count)
                conX['wordCountRange']=np.diff([np.floor(conX['wordCountMin']), np.ceil(conX['wordCountMax'])]) + 1
                print(conX['wordCountMin'], conX['wordCountMax'], conX['wordCountRange'])
            elif len(word_list)==0:
                return render(request, 'search.html', {'error_message': "No responses. Please use different words or settings", 'initForm': 1,  'optRange': range(5,21),})
            return render(request, 'search.html', conX)
        else:
            return render(request, 'search.html', {'error_message': "Please type in some words", 'initForm': 1,  'optRange': range(5,21),})


class ResultsPage(generic.TemplateView):
    template_name = "result.html"
