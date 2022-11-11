from django.urls import path
from . import views
from django.urls import re_path as url


urlpatterns = [
    url(r'^main/(?P<pk>\w+)/$', views.main_page, name='main'),
    url(r'^registration/$', views.register, name='register'),
    url(r'^createproject/$', views.create_project.as_view(), name='create_project'),
    url(r'^myprojects/(?P<pk>\w+)/$', views.my_projects, name='my_projects'),
    url(r'^(?P<pk>\d+)/detail/$', views.ProjectDetail.as_view(), name='detail_project'),
    url(r'^(?P<pk>\d+)/deleteConfirm/$', views.ProjectDeleteConfirm.as_view(), name='delete_project'),
    url(r'^(?P<pk>\d+)/deleteError/$', views.delete_error, name='delete_error'),
    url(r'^changeStatus/$', views.change_status, name='change_status'),
    url(r'^changeStatusConfirm/(?P<pk>\w+)/(?P<st>\w+)/$', views.confirm_status_change, name='confirm_status_change')
]

