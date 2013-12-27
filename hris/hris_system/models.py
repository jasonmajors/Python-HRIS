from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
	user = models.OneToOneField(User)
	last_name = models.CharField(max_length=25)
	first_name = models.CharField(max_length=25)
	hire_date = models.DateField(auto_now=False, auto_now_add=False)
	phone_number = models.CharField(max_length=15, blank=True)
	address = models.CharField(max_length=25, blank=True)
	city = models.CharField(max_length=25, blank=True)
	state = models.CharField(max_length=2, blank=True)
	zipcode = models.IntegerField(blank=True)
	# Not working properly
	DEPT_CHOICES = (
			('New_Hire', 'New Hire'),
			('HRM', 'Human Resources Manager'),
			('HRS', 'Human Resources Specialist'),
			('Dealer', 'Dealer'),
		)

	department = models.CharField(max_length=25, choices=DEPT_CHOICES, default='New_Hire')
	position = models.CharField(max_length=25, default='New_Hire')

	def __unicode__(self):
		return self.user.username

class TimeOffRequest(models.Model):
	employee = models.ForeignKey(Employee)
	date_start = models.DateField(auto_now=False, auto_now_add=False)
	date_end = models.DateField(auto_now=False, auto_now_add=False)
	status = models.CharField(max_length=25, default="PENDING")

	def __unicode__(self):
		return self.employee.user.username

# Will build this out later - need JS powers for calendar.
class Schedule(models.Model):
	#employee = models.ForeignKey(Employee)
	#day = models.DateField(auto_now=False, auto_now_add=False)
	pass		
