from django.views import generic


class HomePage(generic.TemplateView):
    template_name = "home.html"

class AboutPage(generic.TemplateView):
    template_name = "about.html"

# views added by JRJ to develop further
class SearchPage(generic.TemplateView):
    template_name = "search.html"
    def check_sub(self):
        if(request.GET.get('search_thesaurus')):
            some_val = 'did it stick? {0}'.format(request.GET.get('search_words'))
            return HttpResponse('results')

class ResultsPage(generic.TemplateView):
    template_name = "result.html"
