from django.db import models
from django.contrib.auth.models import User

# Will build this out later...
class Schedule(models.Model):
	#day_one_in = models.DateField(auto_now=False, auto_now_add=False)
	#
	pass	
	
class Employee(models.Model):
	user = models.OneToOneField(User)
	#schedule = models.OnetoOneField(Schedule)
	last_name = models.CharField(max_length=25)
	first_name = models.CharField(max_length=25)
	hire_date = models.DateField(auto_now=False, auto_now_add=False)
	phone_number = models.CharField(max_length=15, blank=True)
	address = models.CharField(max_length=25, blank=True)
	city = models.CharField(max_length=25, blank=True)
	state = models.CharField(max_length=2, blank=True)
	zipcode = models.IntegerField(blank=True)

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

	
