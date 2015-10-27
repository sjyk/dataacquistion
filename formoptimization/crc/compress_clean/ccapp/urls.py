from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.home,name='home'),
#	url(r'^(?P<cutoff>.*)-(?P<threshold>.*)-(?P<data_file>.*)-(?P<clustering_func>.*)-(?P<num_groups>.*)',views.viewtree,name='viewtree')
	url(r'^tree',views.viewtree,name='viewtree')
]