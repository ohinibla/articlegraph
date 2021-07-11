from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Site
from .scripts import run

from .scrap_wikipedia import *
from . import alchemy
from . import visjs
from . import wiki_api as api

import time
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class main(View):
    def get(self, request):
        return render(request, 'graph/main.html')
    def post(self, request):
        ctx = {'result': api.get_search_result(request.POST['SEARCHPAGE'])}
        return render(request, 'graph/search_result.html', ctx)
    

# class Result(View):
#     def post(self, request):
#         SEARCHPAGE = self.request.POST['select']
#         if self.request.POST['method'] == 'Inter':
#             rel_method = alchemy.GraphJSON
#         elif self.request.POST['method'] == 'Intra':
#             rel_method = alchemy.IntraGraphJSON_v2
#         rel_method(SEARCHPAGE, file=True)
#         return render(request, 'graph/relations_alchemy.html')
    
class Result(View):
    def post(self, request):
        SEARCHPAGE = self.request.POST['select']
        if self.request.POST['method'] == 'Inter':
            rel_method = visjs.Graph
        elif self.request.POST['method'] == 'Intra':
            rel_method = visjs.IntraGraph_v2
        nodes, edges = rel_method(SEARCHPAGE)
        ctx = {"nodes": nodes, "edges": edges}
        return render(request, 'graph/relations_visjs.html', ctx)  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''   
class IndexView(generic.ListView):
    context_object_name = 'sites'
    template_name = 'graph/index.html'
    
    def get_queryset(self):
        return Site.objects.all()
    
    def post(self, request):
        s = Site_info(request.POST['url'])
        _s = Site(title = s.get_title(), url = request.POST['url'], 
                  synopsis = s.get_synopsis_text(), thumb_img=s.get_title_image())
        _s.save()
        run(_s, s)
        return HttpResponseRedirect(reverse('graph:detail', args=[_s.id]))

def detail(request, pk):
    site = get_object_or_404(Site, pk=pk)
    return render(request, 'graph/detail.html', {'site': site})

class SiteCreateView(CreateView):
    model = Site
    fields = ['url']
    template_name = 'graph/site_form.html'
    
class form_test(View):
    def get(self, request):
        return render(request, 'graph/form_test.html')
    def post(self, request):
        import requests
        S = requests.Session()
        
        URL = "https://en.wikipedia.org/w/api.php"
        
        SEARCHPAGE = request.POST['ftext']
        
        PARAMS = {
            "action": "query",
            "generator": "search",
            "format": "json",
            "gsrsearch": SEARCHPAGE,
            "prop": "info",
            "inprop": "url"
        }
        
        R = S.get(url=URL, params=PARAMS)
        
        DATA = R.json()
        links = []
        for i in DATA['query']['pages']:
            links.append(DATA['query']['pages'][i]['fullurl'])
        ctx = {'links': links}
        return render(request, 'graph/form_test2.html', ctx)

def graph_test(request):
    ctx = {'data': alchemy.graphDict('mazdak', file=True)}
    return render(request, 'graph/graph_test.html', ctx)'''