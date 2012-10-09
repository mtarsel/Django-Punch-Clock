"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from punchclock.models import *



class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

#test user total amounts per week

#for event in allEvent:
#     if event.clock_in > event.clock_out:
#         print('THIS EVENTS SUCKS!')

#go through views and ensure links are 200

class UserTest(TestCase):
	def test_total(self):
		allEvents = ClockEvent.objects.all()
		
		for event in allEvents:
			if not event.testTime():
				print('Crappy time for event with pk=%d' % event.pk)
