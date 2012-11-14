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
def timecards(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="timecards.pdf"'

	buffer = BytesIO()
    # Create the PDF object, using the BytesIO object as its "file."
	p = canvas.Canvas(buffer)
	
	p.setLineWidth(.3)
	p.setFont('Helvetica', 12)
 
	p.drawString(215,778, 'Budgets charged')
	p.drawString(215, 762, 'Example budget')#make the budget charged!!
	p.drawString(360, 778, 'Hours')
	p.drawString(425, 778, 'Rate')
	p.grid([210, 355, 420, 460], [730, 745, 760, 775, 790])

	#x, y, width, height
	p.rect(25, 740, 175, 60, stroke=1, fill=0)
	p.drawString(30,775,'EMPLOYEE TIME REPORT')
	p.drawString(30,760,'For Clarkson Students')
	p.drawString(70,749, 'use only')

	p.drawString(500,773, '12345')#make this the student numbers
	p.line(480,770,580,770)
	p.drawString(500,755,'Student No.')

	p.drawString(500, 733, '11-15-2012')#must be date
	p.line(480,730,580,730)
	p.drawString(480, 718, 'Month   Day   Year')
 
	p.drawString(112, 698, 'Mick Tarsel')#user.firstname, user.lastname
	p.drawString(30,695,'Print name:')
	p.line(92,695,250,695)
	
	p.drawString(395, 698, '10')#total hours
	p.drawString(255,695,'Total Hours Worked:')
	p.line(375,695,490,695)
	
	p.grid([25, 60, 95, 130, 165, 200, 235, 270, 305, 340, 375, 410, 445], [640, 655, 670, 685])
	p.drawString(33, 643, 'Sun')
	p.drawString(68, 643, 'Mon')
	p.drawString(100, 643, 'Tues')
	p.drawString(135, 643, 'Wed')
	p.drawString(166, 643, 'Thurs')
	p.drawString(208, 643, 'Fri')
	p.drawString(243, 643, 'Sat')
	p.drawString(278, 643, 'Sun')
	p.drawString(313, 643, 'Mon')
	p.drawString(345, 643, 'Tues')
	p.drawString(380, 643, 'Wed')
	p.drawString(413, 643, 'Thurs')
	
	p.grid([470, 505, 540], [640, 655, 670, 685])
	p.drawString(478,643, 'Fri')
	p.drawString(513,643, 'Sat')
	
	p.rect(60, 595, 505, 40, stroke=1, fill=0)#make this a grid!!
	
	p.rect(5, 590, 580, 220, stroke=1, fill=0)

	
	elements = []

	data= [['00', '01', '02', '03', '04'],
		['10', '11', '12', '13', '14'],
		['20', '21', '22', '23', '24'],
		['30', '31', '32', '33', '34']]
	t=Table(data,5*[0.4*inch], 4*[0.4*inch])
	
	elements.append(t)

	#p.save(elements)
	
	p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
	p.showPage()
	p.save()

    # Get the value of the BytesIO buffer and write it to the response.
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response


@login_required(login_url= '/manage_login/')
def reports(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="reports.pdf"'

	buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."

	p = canvas.Canvas(buffer)

	p.drawString(30,775,'Account Number')
	p.drawString(30,735,'12345678')

	
	p.drawString(200,778, 'Remaining Balance')
	
	p.drawString(360, 778, 'Spent this semester')



	
	p.drawString(50, 50, "Generated on: DATE")#place the date here!!!

    # Close the PDF object cleanly.
	p.showPage()
	p.save()

    # Get the value of the BytesIO buffer and write it to the response.
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response

