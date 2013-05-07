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

	class Meta:
		ordering = ('priority',)


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
	#pay_rate = models.FloatField()
	start_date = models.DateField(default=datetime.now())
	amount_paid = models.FloatField()
	department = models.ForeignKey(Department)#user can have multiple departments
	account = models.ForeignKey(Account)#can have multiple accounts
	
	in_time = models.TimeField()
	is_in = models.BooleanField(False)
	out_time = models.TimeField()
	active = models.BooleanField(default = True)

	def __unicode__(self):
			return unicode(self.last_name) + ', ' + unicode(self.first_name) + ' : ' + unicode(self.number)

class ClockEvent(models.Model):
	user = models.ForeignKey(User)
	department = models.ForeignKey(Department)
	account = models.ForeignKey(Account, null=True, blank=True)

	def clockIn(self, user, department):
		self.user = user
		self.is_in = user.is_in
		self.in_time = user.in_time
		self.out_time = user.out_time

		self.user = user

		if self.is_in is True:
			print "Error! is_in is True. User is already clocked in!"
			return

		self.department = department
		self.in_time = user.in_time = datetime.now().replace(microsecond=0)
		self.is_in = user.is_in = True

		print "self.in_time is..."
		print self.in_time

		print "self.is_in is ..."
		print self.is_in

		self.save()
		return
		
	def clockOut(self, user, department):

		self.user = user
		self.is_in = user.is_in
		self.in_time = user.in_time
		self.out_time = user.out_time

		if self.is_in is False:
			print "Error! user is clocked out, is_in is False"
			return

		if self.in_time > self.out_time:
			print "Error! in_time is greater than out_time"
			return False

		self.department = department
		self.out_time = user.out_time = datetime.now().replace(microsecond=0)
		self.is_in = user.is_in = False

		print "self.out_time is.."
		print self.out_time

		print "self.is_in is..."
		print self.is_in

		print "self.in_time is..."
		print self.in_time
		#TODO in_time is NONE!!!!

		self.save()
		return

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
