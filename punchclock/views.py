from django.template import Context, loader
from punchclock.models import User
from punchclock.models import ClockEvent
#from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    user_list = User.objects.all().order_by('-last_name')[:5]
    return render_to_response('punchclock/index.html', {'user_list': user_list})
    
    