from django.urls import path
from . import views
from django.urls import re_path as url
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='main'), name='index'),
    url(r'^main/$', views.MainPage.as_view(), name='main'),
    url(r'^registration/$', views.register, name='register'),
    url(r'^createproject/$', views.create_project, name='create_project'),
    url(r'^myprojects/(?P<pk>\w+)/$', views.my_projects, name='my_projects'),
    url(r'^(?P<pk>\d+)/detail/$', views.ProjectDetail.as_view(), name='detail_project'),
    url(r'^(?P<pk>\d+)/deleteConfirm/$', views.ProjectDeleteConfirm.as_view(), name='delete_project'),
    url(r'^(?P<pk>\d+)/deleteError/$', views.delete_error, name='delete_error'),
    url(r'^changeStatus/$', views.change_status, name='change_status'),
    url(r'^changeStatusConfirm/(?P<pk>\w+)/(?P<st>\w+)/$', views.confirm_status_change, name='confirm_status_change'),
    url(r'^changeCategory/$', views.change_category, name="manage_categories"),
    url(r'^categoryDelete/(?P<pk>\w+)/$', views.category_delete, name='category_delete')
]

