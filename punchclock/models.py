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
