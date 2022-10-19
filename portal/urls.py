from django.urls import path
from . import views
from django.urls import re_path as url


urlpatterns = [
    url(r'^$', views.main_page, name='main'),
    url(r'^registration/$', views.register, name='register'),
    url(r'^createproject/$', views.create_project.as_view(), name='create_project'),
    url(r'^myprojects/$', views.my_projects.as_view(), name='my_projects'),
    url(r'^myprojects/(?P<pk>\d+)/detail/$', views.ProjectDetail.as_view(), name='detail_project'),
    url(r'^myprojects/(?P<pk>\d+)/delete/$', views.ProjectDelete.as_view(), name='delete_project')
]

