from django.template import Context, loader
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from punchclock.models import *
from django.template import RequestContext
from datetime import *


from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

#DONT FORGET:
#sudo apt-get install python-pip
#sudo pip install reportlab


def clockIn( request ):
	if request.method == 'POST':
		form = IndexForm( request.POST )
		if form.is_valid():
			instance = form.save( commit=False )
			user = User.objects.get( number=instance.student_number )
			#name = User.objects.get( name=instance.last_name )
			department = Department.objects.get( name=instance.department )
			clock_in = ClockIn()
			clock_in.clockIn( user, department )	
			
		#	if clock_event.clock_in_out( user, department ) is False:
		#		return render_to_response( '404.html')
		
			#print user.in_time

			return render_to_response( 'punchclock/clockin.html', { 'first_name':user.first_name, 'last_name':user.last_name, 'in_time':user.in_time} )
		else:
			to_add = { }
			to_add.update( { 'form': form } )
			print 'Error! user didnt enter a field and hit clock in'
			return render_to_response( '404.html', to_add )
			
	else:
		to_add = { }
		to_add.update( csrf( request ) )
		form = IndexForm()
		to_add.update( { 'form': form } )
		return render_to_response( 'punchclock/index.html', to_add )
	
def clockOut(request):
	if request.method == 'POST':
		form = IndexForm( request.POST )
		if form.is_valid():
			instance = form.save( commit=False )
			user = User.objects.get( number=instance.student_number )
			department = Department.objects.get( name=instance.department )
			clock_out = ClockOut()
			clock_out.clockOut( user, department )
			return render_to_response( 'punchclock/clockout.html', {'first_name': user.first_name, 'last_name': user.last_name, 'out_time':user.out_time} )
		else:
			print 'Error! User didnt enter a field and hit clock out'
			to_add = { }
			to_add.update( { 'form': form } )
			to_add.update( csrf( request ) )
			return render_to_response( '404.html', to_add )


def timecards(request, user ):
	if not request.user.is_authenticated( ):#DOES NOT WORK, STILL ALLOWS USER ENTRY
		return HttpResponseRedirect( '/admin/')	
	
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="timecards.pdf"'

	buffer = BytesIO()
	# Create the PDF object, using the BytesIO object as its "file."
	p = canvas.Canvas(buffer)
	
	p.setLineWidth(.3)
	p.setFont('Courier-Bold', 8.5)
 
	p.drawString(215,778, 'Budgets charged')
	p.drawString(215, 762, '%s') %(user.department)#make Account number!!
	p.drawString(360, 778, 'Hours')
	p.drawString(425, 778, 'Rate')
	p.grid([210, 355, 420, 460], [730, 745, 760, 775, 790])

	#x, y, width, height
	p.rect(25, 740, 175, 60, stroke=1, fill=0)
	p.drawString(55,775,'EMPLOYEE TIME REPORT')
	p.drawString(55,762,'For Clarkson Students')
	p.drawString(95,750, 'use only')

	p.drawString(500,783, '%s') %(user.number)#make this the student numbers
	p.line(480,780,580,780)
	p.drawString(500,773,'Student No.')#770-755

	p.drawString(500, 753, '%s') %(datetime.today()) #must be date
	p.line(480,750,580,750)
	p.drawString(480, 738, 'Month   Day   Year')
 
	p.drawString(112, 708, '%s %%s') %(user.first_name) %(user.last_name)#user.firstname, user.lastname
	p.drawString(30,705,'Print name:')
	p.line(92,705,250,705)
	
	p.drawString(395, 708, '10')#TOTAL HOURS!!!
	p.drawString(255,705,'Total Hours Worked:')
	p.line(375,705,490,705)
		
	##FOR LOOP to start the dates properly.
		
	##Parse dates from Clockin and ClockOut to represent just the dates!!!
	
	p.grid([25, 60, 95, 130, 165, 200, 235, 270, 305, 340, 375, 410, 445], [655, 670, 685, 700])
	p.drawString(33, 658, 'Sun')
	p.drawString(33, 672, '1.5')
	p.drawString(33,688, '11/2')
	
	p.drawString(68, 658, 'Mon')
	p.drawString(68, 672, '0')
	p.drawString(68,688, '11/3')
	
	p.drawString(100, 658, 'Tues')
	p.drawString(135, 658, 'Wed')
	p.drawString(166, 658, 'Thurs')
	p.drawString(208, 658, 'Fri')
	p.drawString(243, 658, 'Sat')
	p.drawString(278, 658, 'Sun')
	p.drawString(313, 658, 'Mon')
	p.drawString(345, 658, 'Tues')
	p.drawString(380, 658, 'Wed')
	p.drawString(413, 658, 'Thurs')
	
	p.grid([470, 505, 540], [655, 670, 685, 700])
	p.drawString(478,658, 'Fri')
	p.drawString(513,658, 'Sat')
	
	p.rect(60, 595, 505, 40, stroke=1, fill=0)
	p.grid([60, 305, 565 ], [595, 618])
	p.drawString(125, 623, 'Work was performed in a satisfactory manner. IAW CFR 175.19.')
	p.drawString(65, 598, 'Student Signature')
	p.drawString(310, 598, 'Dept. Head Signature')
		
	p.rect(5, 590, 580, 220, stroke=1, fill=0)
	
	p.drawString(100, 100, "Hello world.")

	# Close the PDF object cleanly.
	p.showPage()
	p.save()
	
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response
