from django.db import models
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.forms import ModelForm
from django.shortcuts import render_to_response
from datetime import *

from django.core.mail import send_mail


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
        pay_rate = models.FloatField()
        start_date = models.DateField(default=datetime.now())
        amount_paid = models.FloatField()
        department = models.ForeignKey(Department)#user can have multiple departments
        account = models.ForeignKey(Account)#can have multiple accounts
        in_time = models.TimeField()
        is_in = models.BooleanField(False)
        out_time = models.TimeField()
        is_out = models.BooleanField(False)
        active = models.BooleanField(default = True)



        #if they work for one year, increase pay by $0.25

        #one_year = models.DateField(default= start_date +timedelta(days=365))
        #one_year = models.DateTimeField(default=start_date + timedelta(days=365))
        #one_year = models.DateTimeField(default=start_date(start_date.year + 1))
        #one_year = start_date.replace(year = start_date.year + 1)

        #one_year = date.today().replace(year = date.today().year + 1)
        #TODO the example above works, pay rate will never increase. must make date.today = start_date

        #if ( one_year == date.today() ):
        #       pay_rate = pay_rate + 0.25

        def __unicode__(self):
                return unicode(self.last_name) + ', ' + unicode(self.first_name) + ' : ' + unicode(self.number)

class ClockEvent(models.Model):
        user = models.ForeignKey(User)
        department = models.ForeignKey(Department)
        account = models.ForeignKey(Account, null=True, blank=True)

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

                print "self.in_time is..."
                print self.in_time
#TODO in_time is NONE!!!!
                #2013-04-15 14:12:24

                fmt = "%Y-%m-%d %H:%M:%S"
               #d2 = datetime.strptime(self.out_time, fmt)
               # d1 = datetime.strptime(self.in_time, fmt)
               # total_hours = (d2-d1).days * 24 * 60

               # print "total_hours is..."
               # print total_hours

               # ten_hours = datetime.timedelta(hours=10)

                #if total > ten_hours:
                 #       print "user clocked in over ten hours. forgot to clock out"
                  #      clock_out = ClockOut()
                   #     clock_out = clockOut(user, department)
                    #    return


                self.save()
                return

        def payment(self, user):

                Account.objects.all().order_by('-priority')

                self.account = user.account.total
                self.payed = user.pay_rate * Timecard_Management.user.clockedin_hours(user, department)

                if user.accont.priority is 100 and user.account.total > 100:
                        subtract_account = self.payed - self.account

                elif user.account.total <= 100:
                        print "users account has less than $100. switch to next highest priority account"

                        #email someone or make some sort of warning!
                        # go to next account. store accounts in list of variable size???

                        t = loader.get_template('registration/email.txt')
                        c = Context({
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'user_balance': user.account,
                        })
                        #TODO send_mail('Low Balance for Student Worker', t.render(c), 'myemail@gmail.com', ['mystudentemail@clarkson.edu'], fail_silently=False)
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
   # in_time = models.DateField()

class IndexForm( ModelForm ):
        class Meta:
                model = Index

