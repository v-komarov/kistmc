#coding:utf-8
import	datetime
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	ReportSpecForm
from	kis.lib.tmc_report	import	ReportSpecData



### --- Отчет ---
def	ReportSpec(request):


    try:
	if CheckAccess(request,'2') != 'OK':
	    return render_to_response("tmc/notaccess/tmc.html")
    except:
	return HttpResponseRedirect('/')

    if request.method == 'POST':
	form = ReportSpecForm(request.POST)
	if form.is_valid():
	    chief = form.cleaned_data['chief']
	    start_date = form.cleaned_data['start_date']
	    end_date = form.cleaned_data['end_date']

	    response = HttpResponse(mimetype="application/ms-excel")
	    response['Content-Disposition'] = 'attachment; filename=report.xls'
	    return ReportSpecData(response,chief,start_date,end_date)




    form = ReportSpecForm(None)

    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("tmc/reportspec.html",c)

