from django.template import Context, loader
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect
from punchclock.models import *


def index(request):
	department_list = User.objects.all().order_by('-department')[:13]
	return render_to_response('punchclock/index.html', {'department_list': department_list})

def clockin(request):
	
	c ={}
	
	#department_list = User.objects.all().order_by('-department')[:13]
	
	#choose the department they selected
	
	clockin = ClockEvent()
	
	clockin.clockin(username,department)
	
	c.update(csrf(request))

	return render_to_response('punchclock/clockin.html', context_instance=RequestContext(request)) #{'department_list': department_list}, c)	
    
  #TODO LIST
  #1. CALL CLOCKIN FUNCTION = CREATE CUSTOM USER TEMPLATE
  #2. LOAD THE MANAGER PERMISSIONS TO MANAGER PAGE
  #3. GENERATE REPORTS IN HTML FOR MANAGER/MODELS - block the /reports/ page!!!!
  #4. bootstrap design
 
