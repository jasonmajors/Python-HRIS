import datetime

from django.db import models
from django.contrib.auth.models import User


END_TIME = datetime.time(hour=17, minute=0, second=0, microsecond=0)
START_TIME = datetime.time(hour=9, minute=0, second=0, microsecond=0)

class Schedule(models.Model):
	monday_in = models.TimeField(default=START_TIME, null=True, blank=True)
	monday_out = models.TimeField(default=END_TIME, null=True, blank=True)
	tuesday_in = models.TimeField(default=START_TIME, null=True, blank=True)
	tuesday_out = models.TimeField(default=END_TIME, null=True, blank=True)
	wednesday_in = models.TimeField(default=START_TIME, null=True, blank=True)
	wednesday_out = models.TimeField(default=END_TIME, null=True, blank=True)
	thursday_in = models.TimeField(default=START_TIME, null=True, blank=True)
	thursday_out = models.TimeField(default=END_TIME, null=True, blank=True)
	friday_in = models.TimeField(default=START_TIME, null=True, blank=True)
	friday_out = models.TimeField(default=END_TIME, null=True, blank=True)
	saturday_in = models.TimeField(default=None, null=True, blank=True)
	saturday_out = models.TimeField(default=None, null=True, blank=True)
	sunday_in = models.TimeField(default=None, null=True, blank=True)
	sunday_out = models.TimeField(default=None, null=True, blank=True)

	
class Employee(models.Model):
	user = models.OneToOneField(User)
	schedule = models.OneToOneField(Schedule)
	last_name = models.CharField(max_length=25)
	first_name = models.CharField(max_length=25)
	hire_date = models.DateField(auto_now=False, auto_now_add=False)
	phone_number = models.CharField(max_length=15, null=True, blank=True)
	address = models.CharField(max_length=25, null=True, blank=True)
	city = models.CharField(max_length=25, null=True, blank=True)
	state = models.CharField(max_length=2, null=True, blank=True)
	zipcode = models.IntegerField(null=True, blank=True)
	email = models.CharField(max_length=35, null=True, blank=True, default='jasonrmajors@gmail.com')
	DEPT_CHOICES = (
			('New Hire', 'New Hire'),
			('Human Resources', 'Human Resources'),
			('Shift Manager', 'Shift Manager'),
			('Staff', 'Staff'),
			('IT', 'IT Staff'),
		)

	department = models.CharField(max_length=25, choices=DEPT_CHOICES, default="New Hire")
	position = models.CharField(max_length=25, default='New Hire')

	STATUS_CHOICES = (
		('Active', 'Active'),
		('Terminated', 'Terminated'),
		('Paid Time Off', 'Paid Time Off'),
		('Personal Time Off', 'Personal Time Off'),
		('Leave of Absense', 'Leave of Absense' ),
	)
	status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="Active")

	def __unicode__(self):
		return self.user.username

class TimeOffRequest(models.Model):
	employee = models.ForeignKey(Employee)
	date_start = models.DateField(auto_now=False, auto_now_add=False)
	date_end = models.DateField(auto_now=False, auto_now_add=False)
	status = models.CharField(max_length=25, default="PENDING")
	handler = models.CharField(max_length=25)
	comments = models.CharField(max_length=25)

	def __unicode__(self):
		return self.employee.user.username

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	first_time_user = models.BooleanField(default=True)

	def __unicode__(self):
		return self.user.username
