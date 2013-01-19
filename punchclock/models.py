from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.forms import ModelForm
from django.shortcuts import render_to_response

class Account(models.Model):
	name = models.CharField(max_length=512)
	number = models.CharField(max_length=512)
	priority = models.IntegerField()
	total = models.IntegerField()		
	
	def __unicode__(self):
		return unicode(self.name)
		
class Department(models.Model):
	name = models.CharField(max_length=512)
	#students can have 2 departments with same payrate
	
	def __unicode__(self):
		return unicode(self.name)

class User(models.Model):
	number = models.IntegerField(max_length=8)
	first_name = models.CharField(max_length=512)
	last_name = models.CharField(max_length=512)
	pay_rate = models.FloatField()
	start_date = models.DateField()
	amount_paid = models.FloatField()
	department = models.ForeignKey(Department)#user can have multiple departments
	account = models.ForeignKey(Account)#can have multiple accounts
	
	#if they work for one year, increase pay by $0.25
	
	def __unicode__(self):
		return unicode(self.last_name) + ', ' + unicode(self.first_name) + ':' + unicode(self.number) + ' $' + unicode(self.pay_rate)
		

class Timecard(models.Model):
	user = models.ForeignKey(User)
	
	def generate_timecards(self):
	# Create the HttpResponse object with the appropriate PDF headers.
		response = HttpResponse(mimetype='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="timecards.pdf"'

		buffer = BytesIO()
		# Create the PDF object, using the BytesIO object as its "file."
		p = canvas.Canvas(buffer)
	
		p.setLineWidth(.3)
		p.setFont('Courier-Bold', 8.5)
 
		p.drawString(215,778, 'Budgets charged')
		p.drawString(215, 762, 'Example budget')#make the budget charged!!
		p.drawString(360, 778, 'Hours')
		p.drawString(425, 778, 'Rate')
		p.grid([210, 355, 420, 460], [730, 745, 760, 775, 790])

		#x, y, width, height
		p.rect(25, 740, 175, 60, stroke=1, fill=0)
		p.drawString(55,775,'EMPLOYEE TIME REPORT')
		p.drawString(55,762,'For Clarkson Students')
		p.drawString(95,750, 'use only')

		#p.drawString(500,783, str(User.number))#make this the student numbers
		p.line(480,780,580,780)
		p.drawString(500,773,'Student No.')#770-755

		p.drawString(500, 753, '11-15-2012')#must be date
		p.line(480,750,580,750)
		p.drawString(480, 738, 'Month   Day   Year')
 
		p.drawString(112, 708, 'Mick Tarsel')#user.firstname, user.lastname
		p.drawString(30,705,'Print name:')
		p.line(92,705,250,705)
	
		p.drawString(395, 708, '10')#total hours
		p.drawString(255,705,'Total Hours Worked:')
		p.line(375,705,490,705)
	
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

		# Get the value of the BytesIO buffer and write it to the response.
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response

#class Report(models.Model):

class ClockEvent(models.Model):
	user = models.ForeignKey(User)
	department = models.ForeignKey(Department)
	account = models.ForeignKey(Account, null=True, blank=True)
	in_time = models.DateTimeField( null=True, blank=True )
	out_time = models.DateTimeField( null=True, blank=True )
	pay_rate = models.FloatField()
	#timecard = models.ForeignKey(Timecard)
	
	def clockIn(self, user, department):
		
		if not self.in_time == None:
			return

		self.pay_rate = user.pay_rate
		self.department = department
		self.user = user
		self.in_time = timezone.now()
		self.save()
		return #self.in_time
		
	def clockOut(self, user, department):
		
		if not self.out_time == None and not self.in_time == None:
			return 
		
		if self.in_time is None:
			print 'Error!'
			return False
		
		if self.in_time > self.out_time:
			print 'error'
			return False

		self.user = user
		self.pay_rate = user.pay_rate
		self.department = department
		self.out_time = timezone.now()
		#td = self.out_time - clockIn.in_time
		#print td
		#timecard = Timecard.objects.get(user = user)
		#self.timecard = timecard #user.timecard_set[0].clockevent.set out_time != NULL
		self.save()
		return
		
	def hours(account, self):
		td = self.out_time - self.in_time
		return float(td.total_seconds()/3600)	
		
	def amount_payed(self):
		return self.pay_rate * self.hours()
	
	def account_manage(amount_payed, account, self):
		self.account = account
		self.amount_payed = amount_payed
		return self.amount_payed - self.account		
	
	def __unicode__(self):
		return unicode(self.last_name) + ', ' + unicode(self.first_name) + ':' + unicode(self.number)

# choices
DEPARTMENT_CHOICES = (
    ( 'Web Design', 'Web Design' ),
    ( 'Front Desk', 'Front Desk' ),
    ( 'Circulation Desk' , 'Circulation Desk'),
    ( 'ILL', 'ILL'),
    ( 'Cataloging', 'Cataloging'),
    ( 'Digitization' , 'Digitization'),
    ( 'LHR', 'LHR'),
    ( 'Stack Management', 'Stack Management'),
    ( 'Serials', 'Serials'),
    ( 'Acquisitions', 'Acquisitions'),
    ( 'Reference', 'Reference'),
    ( 'Health Sciences', 'Health Sciences'),
    ( 'Media' , 'Media'),
    ( 'Archives', 'Archives'),
)

class Index( models.Model ):
    student_number = models.IntegerField( max_length=8 )
    department = models.CharField( max_length=40, choices=DEPARTMENT_CHOICES )

class IndexForm( ModelForm ):
	class Meta:
		model = Index
