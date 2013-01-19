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
			#name = User.objects.get( name=instance.last_name )
			department = Department.objects.get( name=instance.department )
			clock_event = ClockEvent( )
			clock_event.clockIn( user, department )	
			
			if clock_event.clockIn( user, department ) is False:
				return render_to_response( '404.html')

			return render_to_response( 'punchclock/clockin.html', { 'first_name':user.first_name, 'last_name':user.last_name} )
		else:
			to_add = { }
			to_add.update( { 'form': form } )
			return render_to_response( '404.html', to_add )
			
	else:
		to_add = { }
		to_add.update( csrf( request ) )
		form = IndexForm( )
		to_add.update( { 'form': form } )
		return render_to_response( 'punchclock/index.html', to_add )
	
def clockout(request):
	if request.method == 'POST':
		form = IndexForm( request.POST )
		if form.is_valid( ):
			instance = form.save( commit=False )
			user = User.objects.get( number=instance.student_number )
			department = Department.objects.get( name=instance.department )
			clock_event = ClockEvent( )
			clock_event.clockOut( user, department )
			return render_to_response( 'punchclock/clockout.html', {'first_name': user.first_name, 'last_name':user.last_name} )
		else:
			print 'Error!'
			to_add = { }
			to_add.update( { 'form': form } )
			to_add.update( csrf( request ) )
			return render_to_response( '404.html', to_add )
