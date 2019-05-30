#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


from admina.views import MTSGroup, FinGroup, DelUserGroup, Range
from admina.jsondata import get_json


urlpatterns = [
    url(r'mtsgroup', MTSGroup),
    url(r'fingroup', FinGroup),
    url(r'range', Range),
    url(r'delusergroup', DelUserGroup),
    url(r'jsondata', get_json),

]

