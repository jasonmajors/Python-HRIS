from django.conf.urls import patterns, url
from hris_system import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^submit/$', views.submit, name='submit'),
		url(r'^timeoff/$', views.get_timeoff_requests, name='requests'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^add_employee/$', views.add_employee, name='add_employee'),
		)