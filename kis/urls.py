from django.conf.urls import patterns, include, url
from	django.contrib.staticfiles.urls	import	staticfiles_urlpatterns
from	django.conf	import	settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kis.views.home', name='home'),
    # url(r'^kis/', include('kis.foo.urls')),

    url(r'^$', 'start.views.Home', name='Home'),
    url(r'^exit/$', 'start.views.Exit', name='Exit'),


    url(r'^tmc/$', 'tmc.views.ListTmc', name='ListTmc'),
    url(r'^tmcnew/$', 'tmc.views.TmcNew', name='TmcNew'),
    url(r'^tmcedit/$', 'tmc.views.TmcEdit', name='TmcEdit'),
    url(r'^tmcdata/$', 'tmc.tmcdata1.TmcData1', name='TmcData1'),
    url(r'^tmcdata2/$', 'tmc.tmcdata2.TmcData2', name='TmcData2'),
    url(r'^tmcdata3/$', 'tmc.tmcdata3.TmcData3', name='TmcData3'),
    url(r'^tmcdata4/$', 'tmc.tmcdata4.TmcData4', name='TmcData4'),
    url(r'^tmcdata5/$', 'tmc.tmcdata5.TmcData5', name='TmcData5'),
    url(r'^tmcdata6/$', 'tmc.tmcdata6.TmcData6', name='TmcData6'),
    url(r'^tmcdata7/$', 'tmc.tmcdata7.TmcData7', name='TmcData7'),
    url(r'^tmcnewspec/$', 'tmc.tmcdata1.NewSpec', name='NewSpec'),
    url(r'^tmcspecedit/$', 'tmc.tmcdata1.EditSpec', name='EditSpec'),

    url(r'^tmcopt/$', 'tmc.opt.Finance', name='Finance'),
    url(r'^tmcopt2/$', 'tmc.opt.Logistic', name='Logistic'),

    url(r'^tmcorderlist/$', 'tmc.internalorder.List', name='List'),
    url(r'^tmcordernew/$', 'tmc.internalorder.New', name='New'),
    url(r'^tmcorderspec/$', 'tmc.internalorder.Spec', name='Spec'),
    url(r'^tmcorderprint/$', 'tmc.internalorder.OrderPrint', name='OrderPrint'),

    url(r'^tmcreports/$', 'tmc.reports.ReportSpec', name='ReportSpec'),
    url(r'^tmctocsv/$', 'kis.lib.tmc_csv.GetCsvData', name='GetCsvData'),


    url(r'^admina/', include('admina.urls')),

    url(r'^jsondata/', 'tmc.jsondata.get_json'),
    url(r'^proj/', 'tmc.views.ProjSpec'),

    url(r'css/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/task/kis/kis/static/css/',}),
    url(r'js/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/task/kis/kis/static/js/',}),
    url(r'fonts/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/task/kis/kis/static/fonts/',}),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
