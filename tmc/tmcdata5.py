#coding:utf-8
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	kis.lib.tmc		import	GetTmcData,GetLastStatus
from	kis.lib.tmc_mail	import	Email2Ruk
from	forms			import	EmailForm




### --- Отправка запроса подписи руководителю ---
def	TmcData5(request):

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
	form = EmailForm(request.POST)
	if form.is_valid():
	    email = form.cleaned_data['email']
	    Email2Ruk(email,tmc_id)



    d = GetTmcData(tmc_id)

    form = EmailForm(None)

    s = GetLastStatus(tmc_id)

    c = RequestContext(request,{'d':d,'form':form,'s':s})
    c.update(csrf(request))
    return render_to_response("tmc/tmcdata5.html",c)


