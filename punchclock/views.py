from django.template import Context, loader
from punchclock.models import User
#from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    department_list = User.objects.all().order_by('-department')[:5]
    return render_to_response('punchclock/index.html', {'department_list': department_list})
    
    