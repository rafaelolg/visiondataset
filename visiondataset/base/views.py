""" Views for the base application """

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import UserProfile

import urls

def home(request):
    """ Default view for the root """
    return render_to_response('base/home.html',
        context_instance=RequestContext(request))


@login_required
def autocomplete_users(request):
    q = request.GET.get('q', '')
    profiles = UserProfile.objects.filter(user__username__icontains=q)
    output = ""
    for profile in profiles:
        linha = "%(username)s|<img src='%(mugshot)s'/>%(username)s<br/>%(fullname)s\n" % {
                'username': profile.user.username,
                'mugshot': profile.get_mugshot_url(),
                'fullname': profile.get_full_name_or_username()}
        output = output + linha
    print output
    return HttpResponse(output, mimetype='text/plain')
