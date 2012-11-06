from django.template import Context, loader
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from punchclock.models import *


def index(request):
	department_list = User.objects.all().order_by('-department')[:13]
	return render_to_response('punchclock/index.html', {'department_list': department_list})

@login_required
def clockin_user(request):
	c ={}
	c.update(csrf(request))
	department_list = User.objects.all().order_by('-department')[:13]

	username = password = ''
	if request.POST:
		username = request.POST.get('number')
		password = request.POST.get('department')

		user = authenticate(username=number, password=department)
		
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "You're successfully logged in!"
			else:
				state = "Your account is not active, please contact the site admin."
		else:
			state = "Your username and/or password were incorrect."

	return render_to_response('punchclock/index.html', {'department_list': department_list}, {'state':state, 'number': username})	

def clockin(request):
	return render_to_response('punchclock/clockin.html')
    
    