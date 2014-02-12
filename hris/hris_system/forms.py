from django import forms
from django.contrib.auth.models import User
from hris_system.models import TimeOffRequest, Employee, Schedule

# TODO: Form needs to accept AM/PM formats instead of just military time...
class ScheduleForm(forms.ModelForm):
	monday_in = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="Monday Start Time")
	monday_out = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="Monday Leave Time")
	tuesday_in = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="Tuesday Start Time")
	tuesday_out = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="Tuesday Leave Time")
	wednesday_in = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="Wednesday Start Time")
	wednesday_out = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="Wednesday Leave Time")
	thursday_in = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="Thursday Start Time")
	thursday_out = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),help_text="Thursday Leave Time")
	friday_in = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),help_text="Friday Start Time")
	friday_out = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),help_text="Friday Leave Time")
	saturday_in = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),help_text="Saturday Start Time")
	saturday_out = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),help_text="Saturday Leave Time")
	sunday_in = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),help_text="Sunday Start Time")
	sunday_out = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),help_text="Sunday Leave Time")

	class Meta:
		model = Schedule


class TimeOffRequestForm(forms.ModelForm):
	date_start = forms.DateField(help_text="Please enter the beginning date of your time off request (mm/dd/yyyy).")
	date_end = forms.DateField(help_text="Please enter the final day of your request (mm/dd/yyyy).")
	status = forms.CharField(widget=forms.HiddenInput(), max_length=25, initial="PENDING")

	class Meta:
		model = TimeOffRequest
		fields = ('date_start', 'date_end', 'status')

class EmployeeForm(forms.ModelForm):		
	last_name = forms.CharField(max_length=25, help_text="Employee's LAST NAME")
	first_name = forms.CharField(max_length=25, help_text="Employee's FIRST NAME")
	position = forms.CharField(max_length=25, help_text="Employee's POSITION")
	DEPT_CHOICES = (
			('New Hire', 'New Hire'),
			('Human Resources', 'Human Resources'),
			('Shift Manager', 'Shift Manager'),
			('Staff', 'Staff'),
			('IT', 'IT Staff'),

		)
	department = forms.ChoiceField(choices=DEPT_CHOICES, help_text="Department", initial="New Hire")
	hire_date = forms.DateField(help_text="Employee's hire date")
	phone_number = forms.CharField(max_length=15, help_text="Phone number")
	address = forms.CharField(max_length=25, help_text="Street address")
	city = forms.CharField(max_length=25, help_text="City")
	state = forms.CharField(max_length=2, help_text="State")
	zipcode = forms.IntegerField(help_text="Zipcode")
	email = forms.CharField(max_length=35, help_text="Email Address", initial="jasonrmajors@gmail.com")
	
	STATUS_CHOICES = (
			('Active', 'Active'),
			('Terminated', 'Terminated'),
			('Paid Time Off', 'Paid Time Off'),
			('Personal Time Off', 'Personal Time Off'),
			('Leave of Absense', 'Leave of Absense' ),
		)
	status = forms.ChoiceField(choices=STATUS_CHOICES, initial='Active', help_text="Employment Status")
	
	class Meta:
		model = Employee
		fields = ('last_name', 
				'first_name', 
				'position',
				'department', 
				'hire_date', 
				'phone_number',
				'address',
				'city',
				'state',
				'zipcode',
				'status',

				)