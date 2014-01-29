from collections import Counter
from datetime import date, timedelta

import numpy as np
import matplotlib.pyplot as plt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from hris_system.forms import TimeOffRequestForm, EmployeeForm, ScheduleForm
from hris_system.models import TimeOffRequest, Employee, Schedule, UserProfile 



def hr_or_mgr(user):
	# Returns True if user is a Shift Manager or HR. This is used for access to certain pages.
	return user.groups.filter(name="Shift Manager").exists() or user.groups.filter(name="Human Resources").exists()

def index(request):
	context = RequestContext(request)
	context_dict = {}

	if request.user.is_authenticated():
		employee_list = get_employee_list()
		hr_user = request.user.groups.filter(name="Human Resources").exists()
		mgr_user = request.user.groups.filter(name="Shift Manager").exists()

		employees = Employee.objects.order_by('-hire_date')[:5]
		
		# The user may not be an "employee". Such as an administrative account.
		try:
			employee = Employee.objects.get(user=request.user)
			context_dict['employee'] = employee
			profile = UserProfile.objects.get(user=request.user)
			
			if profile.first_time_user:
				print 'new user'
				return HttpResponseRedirect('/hris/update_password')
		except:
			pass
		# Saves a .png file of the latest hire date data.
		graph_hire_dates()

		context_dict['employees'] = employees
		context_dict['hr_user'] = hr_user
		context_dict['mgr_user'] = mgr_user
		context_dict['employee_list'] = employee_list
		

		return render_to_response('hris_system/index.html', context_dict, context)

	else:
		return HttpResponseRedirect('/hris/login')

def update_password(request):
	context = RequestContext(request)
	context_dict = {}
	user = request.user
	profile = UserProfile.objects.get(user=user)

	failed_attempt = False

	if request.method == 'POST':
		new_password = request.POST['new_password']
		new_password_confirm = request.POST['new_password_confirm']
		
		if new_password == new_password_confirm:
			if len(new_password) > 7:
				user.set_password(new_password)
				profile.first_time_user = False

				profile.save()
				user.save()

				return HttpResponseRedirect('/hris/')

		else:
			failed_attempt = True
			context_dict['failed_attempt'] = failed_attempt

			return render_to_response('hris_system/update_password.html', context_dict, context)

	else:
		return render_to_response('hris_system/update_password.html', context_dict, context)

@login_required
def submit_timeoff(request):
	context = RequestContext(request)
	context_dict = {}
	hr_user = request.user.groups.filter(name="Human Resources").exists()
	mgr_user = request.user.groups.filter(name="Shift Manager").exists()
	employee_list = get_employee_list()

	if request.method == 'POST':
		form = TimeOffRequestForm(request.POST)

		if form.is_valid():
			time_off_request = form.save(commit=False)
			employee = Employee.objects.get(user=request.user)
			time_off_request.employee = employee
			time_off_request.save()

			return index(request)
		else:
			print form.errors
	else:
		form = TimeOffRequestForm()

	context_dict['form'] = form
	context_dict['hr_user'] = hr_user
	context_dict['mgr_user'] = mgr_user
	context_dict['employee_list'] = employee_list

	return render_to_response('hris_system/submit.html', context_dict, context)				

def user_login(request):
	context = RequestContext(request)
	failed_attempt = False

	if request.method == 'POST':
		# Information from the login form.
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)

				return HttpResponseRedirect('/hris/')

			else:
				disabled = True

				return render_to_response("hris_system/login.html", {"disabled": disabled}, context)	
				
		else:
			failed_attempt = True

			print "Invalid login: {0}, {1}".format(username, password)

			return render_to_response("hris_system/login.html", {"failed_attempt": failed_attempt}, context)

	else:
		return render_to_response('hris_system/login.html', {}, context)				

@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/hris/')

@user_passes_test(hr_or_mgr)
def get_timeoff_requests(request, request_status):
	context = RequestContext(request)
	context_dict = {}
	employee_list = get_employee_list()
	hr_user = request.user.groups.filter(name="Human Resources").exists()
	mgr_user = request.user.groups.filter(name="Shift Manager").exists()

	status = request_status.upper()
	buttons = False

	#Only need "Approve" or "Deny" request buttons if the status is pending.
	if status == "PENDING":
		buttons = True

	# Get either pending, approved, or denied timeoff requests depending on what URL is passed.
	timeoff_requests = TimeOffRequest.objects.filter(status=status).order_by('-id')

	context_dict['employee_list'] = employee_list
	context_dict['hr_user'] = hr_user
	context_dict['mgr_user'] = mgr_user
	context_dict['timeoff_requests'] = timeoff_requests
	context_dict['status'] = status
	context_dict['buttons'] = buttons

	return render_to_response('hris_system/timeoff.html', context_dict, context)

@login_required
def handle_timeoff(request):
	"""A function called to either approve or deny a pending timeoff requests."""

	context = RequestContext(request)
	context_dict = {}
	request_id = None
	

	user = request.user.username.replace('_', ' ')
	# Even though this function is only activated when a request is approved or denied,
	# the pending timeoff requests must be fetched and added to the context_dict so they
	# can be passed to the template.
	timeoff_requests = TimeOffRequest.objects.filter(status="PENDING")

	context_dict['timeoff_requests'] = timeoff_requests

	if request.method == "GET":
		request_id = request.GET['request_id']
		# Returns either "APPROVED" or "DENIED".
		approve_or_deny = request.GET['approve_or_deny']
		if request_id:
			t_request = TimeOffRequest.objects.get(id=int(request_id))
			t_request.status = approve_or_deny
			t_request.handler = user
			t_request.save()

	return render_to_response('hris_system/timeoff_requests.html', context_dict, context)	


@user_passes_test(hr_or_mgr)
def add_employee(request):
	context = RequestContext(request)
	context_dict = {}
	hr_user = request.user.groups.filter(name="Human Resources").exists()
	mgr_user = request.user.groups.filter(name="Shift Manager").exists()
	employee_list = get_employee_list()

	if request.method == "POST":
		form = EmployeeForm(request.POST)
		profile = UserProfile()

		if form.is_valid():
			
			employee = form.save(commit=False)
			# Create login credentials.
			username = employee.first_name + "_" + employee.last_name
			new_user = User.objects.create_user(username=username, password="password")
			new_user.first_name = employee.first_name
			new_user.last_name = employee.last_name
			new_user.save()

			employee.user = new_user
			profile.user = new_user
			profile.save()

			# NOTE: Schedules should be added by managers -- default for development purposes!
			default_schedule = Schedule()
			default_schedule.save()
			employee.schedule = default_schedule

			# Create/assign user groups based on employee department.
			assigned_group, c = Group.objects.get_or_create(name=employee.department)
			assigned_group.user_set.add(employee.user)

			employee.save()

			return index(request)
		else:
			print form.errors
	else:
		form = EmployeeForm()

	context_dict['form'] = form
	context_dict['employee_list'] = employee_list
	context_dict['hr_user'] = hr_user
	context_dict['mgr_user'] = mgr_user

	return render_to_response('hris_system/add_employee.html', context_dict, context)

def get_employee_list(max_results=0, starts_with=''):
	employee_list = []

	if starts_with:
		employee_list = Employee.objects.filter(last_name__startswith=starts_with)
	else:
		employee_list = Employee.objects.all().order_by("last_name")

	if max_results > 0:
		if len(employee_list) >	max_results:
			employee_list = employee_list[:max_results]

	return employee_list

def suggest_employee(request):
	context = RequestContext(request)
	context_dict = {}
	employee_list = []
	starts_with = ''

	if request.method == "GET":
		starts_with = request.GET['suggestion']
	else:
		starts_with = request.POST['suggestion']

	employee_list = get_employee_list(8, starts_with)
	
	context_dict['employee_list'] = employee_list

	return render_to_response('hris_system/employee_list.html', context_dict, context)				

def test_for_timeoff(employee):
	timeoff_requests = TimeOffRequest.objects.filter(employee=employee)
	for t in timeoff_requests:
		if t.status == "APPROVED":
			if t.date_start < date.today() and date.today() < t.date_end:
				return True

	return False	

@user_passes_test(hr_or_mgr)
def get_employee_page(request, employee_url):
	context = RequestContext(request)
	context_dict = {}
	hr_user = request.user.groups.filter(name="Human Resources").exists()
	mgr_user = request.user.groups.filter(name="Shift Manager").exists()
	employee = Employee.objects.get(id=employee_url)

	on_leave = test_for_timeoff(employee)
	if on_leave:
		employee.status = 'Personal Time Off'
		employee.save()

	employee_list = get_employee_list()

	context_dict['employee'] = employee
	context_dict['employee_list'] = employee_list
	context_dict['hr_user'] = hr_user
	context_dict['mgr_user'] = mgr_user

	return render_to_response('hris_system/employee_page.html', context_dict, context)

def modify_pto(employee):
	pto_to_modify = []

	timeoff_requests = TimeOffRequest.objects.filter(employee=employee)

	for t in timeoff_requests:
		if t.status == "APPROVED":
			if t.date_start < date.today() and date.today() < t.date_end:
				pto_to_modify.append(t)

	return pto_to_modify

# Managers can still edit employee pages at this point -- TODO: look into Django permissions.
@user_passes_test(hr_or_mgr)
def edit_employee_page(request, employee_url):
	context = RequestContext(request)
	context_dict = {}
	hr_user = request.user.groups.filter(name="Human Resources").exists()
	mgr_user = request.user.groups.filter(name="Shift Manager").exists()
	employee_list = get_employee_list()
	on_pto = False

	employee = Employee.objects.get(id=employee_url)
	if employee.status == "Personal Time Off":
		on_pto = True

	form = EmployeeForm(request.POST or None, instance=employee)
	if form.is_valid():
		employee_changes = form.save(commit=False)
		# Update the employee's user groups with their new department -- if they should no longer have access to their
		# previous department's group, the employee will need this user group removed in the admin interface.
		employee_group, c = Group.objects.get_or_create(name=employee.department)
		employee_group.user_set.add(employee.user)

		if on_pto is True and employee_changes.status != "Personal Time Off":
			pto_to_modify = modify_pto(employee)
			for i in pto_to_modify:
				original_end = i.date_end
				i.date_end = date.today() - timedelta(1)
				i.comments = "PTO end date changed from {0} to {1}.".format(original_end, i.date_end)
				i.save()

		employee_changes.save()

		return HttpResponseRedirect('/hris/')
	
	context_dict['form'] = form
	context_dict['employee'] = employee
	context_dict['employee_list'] = employee_list
	context_dict['hr_user'] = hr_user
	context_dict['mgr_user'] = mgr_user

	return render_to_response('hris_system/edit_employee.html', context_dict, context)

def my_timeoff_requests(request):
	context = RequestContext(request)
	context_dict = {}
	hr_user = request.user.groups.filter(name="Human Resources").exists()
	mgr_user = request.user.groups.filter(name="Shift Manager").exists()
	employee_list = get_employee_list()

	employee = Employee.objects.get(user=request.user)
	timeoff_requests = TimeOffRequest.objects.filter(employee=employee).order_by('-id')

	context_dict['timeoff_requests'] = timeoff_requests
	context_dict['hr_user'] = hr_user
	context_dict['mgr_user'] = mgr_user
	context_dict['employee_list'] = employee_list


	return render_to_response('hris_system/user_timeoff_requests.html', context_dict, context)

def graph_hire_dates():
	employees = Employee.objects.all()

	# Loop through the hire dates and count the freq of each month with a counter dictionary.
	counter = Counter([i.hire_date.month for i in employees])

	# Tuple for the x-axis labels of the graph.
	months = ('Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Ooct', 'Nov', 'Dec')
	# Months in datetime object stored numerically... 1 == Jan, 2 == Feb, etc.
	frequency = [counter[1],
				counter[2],
				counter[3],
				counter[4],
				counter[5],
				counter[6],
				counter[7],
				counter[8],
				counter[9],
				counter[10],
				counter[11],
				counter[12],
				]

	xlocations = np.array(range(len(months))) + 0.5
	width = 0.5
	plt.bar(xlocations, frequency, width=width)
	plt.xticks(xlocations + width/2, months, rotation=90)
	plt.subplots_adjust(bottom=0.15)
	plt.rcParams['figure.figsize'] = 12, 8

	plt.ylim([0, max(frequency) + 1])
	plt.savefig('static/graph.png')


def edit_employee_schedule(request, employee_url):
	context = RequestContext(request)
	context_dict = {}
	hr_user = request.user.groups.filter(name="Human Resources").exists()
	mgr_user = request.user.groups.filter(name="Shift Manager").exists()
	employee_list = get_employee_list()

	employee = Employee.objects.get(id=employee_url)

	form = ScheduleForm(request.POST or None, instance=employee.schedule)
	if form.is_valid():
		employee.schedule = form.save(commit=False)
		employee.schedule.save()

		return HttpResponseRedirect('/hris/')

	context_dict['form'] = form
	context_dict['employee'] = employee
	context_dict['employee_list'] = employee_list
	context_dict['hr_user'] = hr_user
	context_dict['mgr_user'] = mgr_user

	return render_to_response('hris_system/edit_schedule.html', context_dict, context)


