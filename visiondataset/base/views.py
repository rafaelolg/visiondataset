""" Views for the base application """

from django.shortcuts import render_to_response
from django.template import RequestContext
import urls

def show_urls(urllist, depth=0):
    for entry in urllist:
        print "  " * depth, entry.regex.pattern
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)


def home(request):
    """ Default view for the root """
    show_urls(urls.urlpatterns)
    return render_to_response('base/home.html',
        context_instance=RequestContext(request))
