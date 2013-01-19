from django.template import Context, loader
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404, HttpResponseRedirect
from punchclock.models import *

#from django.views.decorators.csrf import csrf_exempt

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


#DONT FORGET:
#sudo apt-get install python-pip
#sudo pip install reportlab

def logout_user(request):
		logout(request)
		return HttpResponseRedirect('/manage/')

#DOES NOT WORK. STATE IS SKETCHY
def login_user(request):
	to_pass = {}
	to_pass.update(csrf(request))
	username = password = ''
	
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "You're successfully logged in!"
				return render_to_response('management/manage.html',{'state':state, 'username': username})
			else:
				state = "Your account is not active, please contact the site admin."
		else:
			state = "Incorrect Username or Password."
			#raise Http404
			return render_to_response('/manage_login/', to_pass, {'state':state, 'username':username})
	else:		
		to_pass.update()
		return render_to_response('manage_login', to_pass, {'state':state, 'username': username})

		
#@login_required(login_url= '/manage_login/')
def manage(request):
	if not request.user.is_authenticated( ):#DOES NOT WORK, STILL ALLOWS USER ENTRY
		return HttpResponseRedirect( '/manage_login/')
	else:
		students = User.objects.all()
		departments = Department.objects.all()
		return render_to_response('management/manage.html')
	

def timecards(request):
	if not request.user.is_authenticated():
		raise Http404
	

def reports(request):
	if not request.user.is_authenticated():
		raise Http404	
	
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="reports.pdf"'

	buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."

    
    #MAKE THIS A TABLE!!!!!
	p = canvas.Canvas(buffer)

	p.drawString(30,775,'Account Number')
	p.drawString(30,735,'12345678')

	
	p.drawString(200,778, 'Total')
	
	p.drawString(360, 778, 'Remaining Balance')
	p.drawString(50, 50, "Generated on: DATE")#place the date here!!!

    # Close the PDF object cleanly.
	p.showPage()
	p.save()

    # Get the value of the BytesIO buffer and write it to the response.
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response

