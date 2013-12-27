from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from hris_system.forms import TimeOffRequestForm, EmployeeForm
from hris_system.models import TimeOffRequest, Employee 


def index(request):
	context = RequestContext(request)
	context_dict = {}
	employee_list = get_employee_list()
	hr_employee = request.user.groups.filter(name="Human Resources").exists()
	mgr_employee = request.user.groups.filter(name="Shift Manager").exists()

	employees = Employee.objects.order_by('-hire_date')[:5]

	context_dict['employees'] = employees
	context_dict['hr_employee'] = hr_employee
	context_dict['mgr_employee'] = mgr_employee
	context_dict['employee_list'] = employee_list

	return render_to_response('hris_system/index.html', context_dict, context)

@login_required
def submit_timeoff(request):
	context = RequestContext(request)
	context_dict = {}
	hr_employee = request.user.groups.filter(name="Human Resources").exists()
	mgr_employee = request.user.groups.filter(name="Shift Manager").exists()

	if request.method == 'POST':
		form = TimeOffRequestForm(request.POST)

		if form.is_valid():
			time_off_request = form.save(commit=False)
			user = User.objects.get(username=request.user)
			employee = Employee.objects.get(user=user)
			
			time_off_request.employee = employee
			time_off_request.save()

			return index(request)
		else:
			print form.errors
	else:
		form = TimeOffRequestForm()

	context_dict['form'] = form
	context_dict['hr_employee'] = hr_employee
	context_dict['mgr_employee'] = mgr_employee

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
				user.hr = user.groups.filter(name="Human Resources").exists()

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

@login_required
def get_timeoff_requests(request, request_status):
	context = RequestContext(request)
	context_dict = {}
	employee_list = get_employee_list()
	hr_employee = request.user.groups.filter(name="Human Resources").exists()
	mgr_employee = request.user.groups.filter(name="Shift Manager").exists()

	status = request_status.upper()
	buttons = False

	#Only need "Approve" or "Deny" request buttons if the status is pending.
	if status == "PENDING":
		buttons = True

	# Get either pending, approved, or denied timeoff requests depending on what URL is passed.
	timeoff_requests = TimeOffRequest.objects.filter(status=status).order_by('-id')

	context_dict['employee_list'] = employee_list
	context_dict['hr_employee'] = hr_employee
	context_dict['mgr_employee'] = mgr_employee
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

	status = "PENDING"
	# Even though this function is only activated when a request is approved or denied,
	# the pending timeoff requests must be fetched and added to the context_dict so they
	# can be passed to the template.
	timeoff_requests = TimeOffRequest.objects.filter(status=status)

	context_dict['status'] = status
	context_dict['timeoff_requests'] = timeoff_requests

	if request.method == "GET":
		request_id = request.GET['request_id']
		# Returns either "APPROVED" or "DENIED".
		approve_or_deny = request.GET['approve_or_deny']

		if request_id:
			t_request = TimeOffRequest.objects.get(id=int(request_id))
			t_request.status = approve_or_deny
			t_request.save()

	return render_to_response('hris_system/timeoff_requests.html', context_dict, context)	


@login_required
def add_employee(request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == "POST":
		form = EmployeeForm(request.POST)

		if form.is_valid():
			
			employee = form.save(commit=False)
			username = employee.first_name + "_" + employee.last_name
			new_user = User.objects.create_user(username=username, password="password")
			employee.user = new_user
			# Dynamically create/assign user groups based on employee position.
			assigned_group, c = Group.objects.get_or_create(name=employee.position)
			assigned_group.user_set.add(employee.user)

			employee.save()

			return index(request)
		else:
			print form.errors
	else:
		form = EmployeeForm()

	return render_to_response('hris_system/add_employee.html', {'form':form}, context)

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

def get_employee_page(request, employee_url):
	context = RequestContext(request)
	context_dict = {}
	employee = Employee.objects.get(id=employee_url)

	employee_list = get_employee_list()

	context_dict['employee'] = employee
	context_dict['employee_list'] = employee_list

	return render_to_response('hris_system/employee_page.html', context_dict, context)





