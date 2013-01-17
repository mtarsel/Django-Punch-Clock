from django.template import Context, loader
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from punchclock.models import *
from django.template import RequestContext

def clockin( request ):
	if request.method == 'POST':
		form = IndexForm( request.POST )
		if form.is_valid( ):
			instance = form.save( commit=False )
			user = User.objects.get( number=instance.student_number )
			department = Department.objects.get( name=instance.department )
			clock_event = ClockEvent( )
			clock_event.clockIn( user, department )	
			return render_to_response( 'punchclock/clockin.html' )
		else:
			print 'Error!'
			raise Http404
			#to_add = { }
			#to_add.update( { 'form': form } )
			#return render_to_response( 'punchclock/index.html', to_add )
			
	else:
		to_add = { }
		to_add.update( csrf( request ) )
		form = IndexForm( )
		to_add.update( { 'form': form } )
		return render_to_response( 'punchclock/index.html', to_add )



#def index(request):
	#department_list = User.objects.all().order_by('-department')[:13]
	
	#c = {'department_list': department_list}
	##c.update(csrf(request))
	
	##clockin = ClockEvent()
	##number = User.objects.number()
	##department = User.objects.department()
	
	##clockin.clockIn(number,department)
	
	#return render_to_response('punchclock/index.html', {'department_list': department_list}, context_instance=RequestContext(request)) 

#def clockin(request):

	#department_list = User.objects.all().order_by('-department')[:13]
	
	#c = {'department_list': department_list}

	#c = {'department_list': department_list}
	
	##user_number = User.number#'Manager' object has no attribute 'number'
	##department = User.objects.department
	
	##clockin = ClockEvent.objects.ClockIn(user_number, department)
	
	##c.update(csrf(request))

	#return render_to_response('punchclock/clockin.html', {'department_list': department_list}, c)	
	
	
def clockout(request):
	if request.method == 'POST':
		form = IndexForm( request.POST )
		if form.is_valid( ):
			instance = form.save( commit=False )
			user = User.objects.get( number=instance.student_number )
			department = Department.objects.get( name=instance.department )
			clock_event = ClockEvent( )
			clock_event.clockOut( user, department )
			return render_to_response( 'punchclock/clockout.html' )
		else:
			print 'Error!'
			to_add = { }
			to_add.update( { 'form': form } )
			to_add.update( csrf( request ) )
			return render_to_response( 'punchclock/index.html', to_add )
