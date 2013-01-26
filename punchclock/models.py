from django.db import models
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.forms import ModelForm
from django.shortcuts import render_to_response
from datetime import *

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

#WANT TO GENERATE A TIMECARD FOR EACH USER

	STATUS_CHOICES = (
    ('g', 'Generate Timecard'),
)

class User(models.Model):
	number = models.IntegerField(max_length=8)
	first_name = models.CharField(max_length=512)
	last_name = models.CharField(max_length=512)
	pay_rate = models.FloatField()
	start_date = models.DateField()
	amount_paid = models.FloatField()
	department = models.ForeignKey(Department)#user can have multiple departments
	account = models.ForeignKey(Account)#can have multiple accounts
	in_time = models.DateField(null = True, blank = True)
	is_in = models.BooleanField(False)
	out_time = models.DateField(null = True)
	is_out = models.BooleanField(False)
	#if they work for one year, increase pay by $0.25
	
	def __unicode__(self):
		return unicode(self.last_name) + ', ' + unicode(self.first_name) + ':' + unicode(self.number) + ' $' + unicode(self.pay_rate)
		
	#THE CODE BELOW WILL CREATE A TIMECARD PDF WITH THE USER FIELDS, MAKE THIS AN ADMIN ACTION SO ADMIN SELECTS WHICH USER (MAYBE ALL) 
	#AND A TIMECARD IS CREATED
		
#class GenerateTimecard(models.Model):
	#user = models.ForeignKey(User)
	#today = datetime.today()
	
#	def __unicode__(self):
#		return self.user
	
	
	#def generate_timecards(self):
	## Create the HttpResponse object with the appropriate PDF headers.
		#response = HttpResponse(mimetype='application/pdf')
		#response['Content-Disposition'] = 'attachment; filename="timecards.pdf"'

		#buffer = BytesIO()
		## Create the PDF object, using the BytesIO object as its "file."
		#p = canvas.Canvas(buffer)
	
		#p.setLineWidth(.3)
		#p.setFont('Courier-Bold', 8.5)
 
		#p.drawString(215,778, 'Budgets charged')
		#p.drawString(215, 762, '%s') %(user.department)#make Account number!!
		#p.drawString(360, 778, 'Hours')
		#p.drawString(425, 778, 'Rate')
		#p.grid([210, 355, 420, 460], [730, 745, 760, 775, 790])

		##x, y, width, height
		#p.rect(25, 740, 175, 60, stroke=1, fill=0)
		#p.drawString(55,775,'EMPLOYEE TIME REPORT')
		#p.drawString(55,762,'For Clarkson Students')
		#p.drawString(95,750, 'use only')

		#p.drawString(500,783, '%s') %(user.number)#make this the student numbers
		#p.line(480,780,580,780)
		#p.drawString(500,773,'Student No.')#770-755

		#p.drawString(500, 753, '%s') %(today) #must be date
		#p.line(480,750,580,750)
		#p.drawString(480, 738, 'Month   Day   Year')
 
		#p.drawString(112, 708, '%s %%s') %(user.first_name) %(user.last_name)#user.firstname, user.lastname
		#p.drawString(30,705,'Print name:')
		#p.line(92,705,250,705)
	
		#p.drawString(395, 708, '10')#TOTAL HOURS!!!
		#p.drawString(255,705,'Total Hours Worked:')
		#p.line(375,705,490,705)
		
		##FOR LOOP to start the dates properly.
		
		##Parse dates from Clockin and ClockOut to represent just the dates!!!
	
		#p.grid([25, 60, 95, 130, 165, 200, 235, 270, 305, 340, 375, 410, 445], [655, 670, 685, 700])
		#p.drawString(33, 658, 'Sun')
		#p.drawString(33, 672, '1.5')
		#p.drawString(33,688, '11/2')
	
		#p.drawString(68, 658, 'Mon')
		#p.drawString(68, 672, '0')
		#p.drawString(68,688, '11/3')
	
		#p.drawString(100, 658, 'Tues')
		#p.drawString(135, 658, 'Wed')
		#p.drawString(166, 658, 'Thurs')
		#p.drawString(208, 658, 'Fri')
		#p.drawString(243, 658, 'Sat')
		#p.drawString(278, 658, 'Sun')
		#p.drawString(313, 658, 'Mon')
		#p.drawString(345, 658, 'Tues')
		#p.drawString(380, 658, 'Wed')
		#p.drawString(413, 658, 'Thurs')
	
		#p.grid([470, 505, 540], [655, 670, 685, 700])
		#p.drawString(478,658, 'Fri')
		#p.drawString(513,658, 'Sat')
	
		#p.rect(60, 595, 505, 40, stroke=1, fill=0)
		#p.grid([60, 305, 565 ], [595, 618])
		#p.drawString(125, 623, 'Work was performed in a satisfactory manner. IAW CFR 175.19.')
		#p.drawString(65, 598, 'Student Signature')
		#p.drawString(310, 598, 'Dept. Head Signature')
		
		#p.rect(5, 590, 580, 220, stroke=1, fill=0)
	
		#p.drawString(100, 100, "Hello world.")

		## Close the PDF object cleanly.
		#p.showPage()
		#p.save()


class ClockIn(models.Model):
	user = models.ForeignKey(User)
	department = models.ForeignKey(Department)
	account = models.ForeignKey(Account, null=True, blank=True)
#	in_time = models.DateTimeField( null=True, blank=True )

		
	def clockIn(self, user, department):
		
		self.user = user
		self.is_out = user.is_out
		
		if self.is_out is True:
			print "Error! is_out is True. User is already clocked out!"
			return
			
		self.pay_rate = user.pay_rate
		self.department = department
		self.in_time = user.in_time = datetime.now().replace(microsecond=0)
		self.is_in = user.is_in = True
		
		print "self.in_time is..."
		print self.in_time
		
		print "self.is_in is ..."
		print self.is_in
		
		print "self.is_out is ..."
		print self.is_out
		
		self.save()
		return
		
class ClockOut(models.Model):
	user = models.ForeignKey(User)
	department = models.ForeignKey(Department)
	account = models.ForeignKey(Account, null=True, blank=True)

	def clockOut(self, user, department):
		
		self.user = user
		self.is_in = user.is_in
		self.is_out = user.is_out
		self.in_time = user.in_time
		self.out_time = user.out_time
		
		if not self.is_in is False:
			print "Error! user is not clocked in, is_in is False"
			return 
			
		if self.is_out is True:
			print 'Error! is_out is true, user already clocked out'
			return False
			
		if self.in_time > self.out_time:
			print "Error! in_time is greater than out_time"
			return False
			
		self.pay_rate = user.pay_rate
		self.department = department
		self.out_time = user.out_time = datetime.now().replace(microsecond=0)
		self.is_out = user.is_out = True
		
		print "self.out_time is.."
		print self.out_time
		
		print "self.is_out is ..."
		print self.is_out
		
		print "self.is_in is..."
		print self.is_in
		
		self.save()
		return

class Timecard_Management(models.Model):
	
	user = models.ForeignKey(User)
	
	def clockedin_hours(self, user, department):
		total = user.out_time - user.in_time
		print "out_time - in_time is %s" %(total)
		
		ten_hours = datetime.timedelta(hours=10)
		
		if total > ten_hours:
			print "user clocked in over ten hours. forgot to clock out"
			clock_out = ClockOut()
			clock_out = clockOut(user, department)
			return 	
		
		return
		
	def payment(self, user):
		
		self.account = user.account.total
		self.payed = user.pay_rate * Timecard_Management.user.clockedin_hours(user, department)
		
		if user.accont.priority is 100 and user.account.total > 100:
			subtract_account = self.payed - self.account
			
		elif user.account.total <= 100:
			print "users account has less than $100. switch to next highest priority account"
			#email someone or make some sort of warning!
			# go to next account. store accounts in list of variable size???
		
		return
		
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
   # in_time = models.DateField()

class IndexForm( ModelForm ):
	class Meta:
		model = Index
