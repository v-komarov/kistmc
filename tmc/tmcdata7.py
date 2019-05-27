#coding:utf-8
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	kis.lib.tmc		import	SetShifr,GetTmcData,GetLastStatus
from	forms			import	ShifrForm




### --- Шифр затрат ---
def	TmcData7(request):

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

    d = GetTmcData(tmc_id)


    if request.method == 'POST':
	form = ShifrForm(request.POST)
	if form.is_valid():
	    shifr = form.cleaned_data['shifr']
	    SetShifr(tmc_id,d[8],GetUserKod(request),shifr)


    d = GetTmcData(tmc_id)

    form = ShifrForm(None)
    form.fields['shifr'].initial = d[23]

    s = GetLastStatus(tmc_id)

    c = RequestContext(request,{'d':d,'form':form,'s':s})
    c.update(csrf(request))
    return render_to_response("tmc/tmcdata7.html",c)


