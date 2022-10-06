from django.urls import path
from . import views
from django.urls import re_path as url


urlpatterns = [
    url(r'^$', views.main_page, name='main'),
    url(r'^registration/$', views.register, name='register')
]