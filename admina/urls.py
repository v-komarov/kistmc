#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


from admina.views import MTSGroup, FinGroup, DelUserGroup



urlpatterns = [
    url(r'mtsgroup', MTSGroup),
    url(r'fingroup', FinGroup),
    url(r'delusergroup', DelUserGroup),

]

