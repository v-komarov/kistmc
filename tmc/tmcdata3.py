#coding:utf-8
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	kis.lib.tmc		import	GetTmcData,GetStatusList,NewTmcStatus,GetStatusHistory,GetLastStatus
from	kis.lib.tmc_mail	import	EmailStatusInfo
from	forms			import	StatusForm




### --- Статусы ---
def	TmcData3(request):

    """
    if CheckAccess(request,'2') != 'OK':
	return render_to_response("tmc/notaccess/tmc.html")
    """

    ## --- Номер заявки ---
    try:
	tmc_id = request.GET['tmc_id']
	request.session['tmc_id'] = tmc_id
    except:
	pass

    try:
	tmc_id = request.session['tmc_id']
    except:
	return HttpResponseRedirect("/tmc")



    if request.method == 'POST':
	form = StatusForm(request.POST)
	if form.is_valid():
	    comment = form.cleaned_data['comment']
	    status = form.cleaned_data['status']
	    r = NewTmcStatus(GetUserKod(request),tmc_id,comment,status)
	    if r == 'OK':
		EmailStatusInfo(tmc_id)


    d = GetTmcData(tmc_id)
    data = GetStatusHistory(tmc_id)

    form = StatusForm(None)
    form.fields['status'].choices = GetStatusList(d[5])

    s = GetLastStatus(tmc_id)

    c = RequestContext(request,{'d':d,'form':form,'data':data,'s':s})
    c.update(csrf(request))
    return render_to_response("tmc/tmcdata3.html",c)


