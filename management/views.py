from django.template import Context, loader
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404

#from django.views.decorators.csrf import csrf_exempt

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle



#DONT FORGET:
#sudo apt-get install python-pip
#sudo pip install reportlab


@login_required(login_url= '/manage_login/')
def manage(request):
	c ={}
	c.update(csrf(request))
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
			return render_to_response('404.html', {'state':state, 'username':username})
			
		
	return render_to_response('management/manage.html',{'state':state, 'username': username})


@login_required(login_url= '/manage_login/')
def reports(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="reports.pdf"'

	buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."

	p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
	#canvas = canvas.Canvas("form.pdf", pagesize=letter)
	
	p.setLineWidth(.3)
	p.setFont('Helvetica', 12)
 
	p.rect(25, 740, 175, 60, stroke=1, fill=0)
	#x, y, width, height

	#p.grid([200, 215, 230], [750, 755, 760])
	
	p.rect(210, 730, 250, 70, stroke=1, fill=0)#make this grid!!

	
	p.drawString(30,775,'EMPLOYEE TIME REPORT')
	p.drawString(30,760,'For Clarkson Students')
	p.drawString(70,749, 'use only')
	
	p.line(480,770,580,770)
	p.drawString(500,755,'Student No.')

	p.line(480,730,580,730)
	p.drawString(480, 718, 'Month   Day   Year')
 
	p.drawString(30,695,'Print name:')
	p.line(92,695,250,695)
	
	p.drawString(255,695,"Total Hours Worked:")
	p.line(375,695,490,695)
	
	p.rect(75, 640, 475, 45, stroke=1, fill=0)#make this a grid!!
	
	p.rect(60, 595, 505, 40, stroke=1, fill=0)#make this a grid!!
	
	p.rect(5, 590, 580, 220, stroke=1, fill=0)

	
	
	p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
	p.showPage()
	p.save()

    # Get the value of the BytesIO buffer and write it to the response.
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response
	

