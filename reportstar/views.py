from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def index(request, runid):
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
