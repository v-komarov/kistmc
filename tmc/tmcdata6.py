#coding:utf-8
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	kis.lib.tmc		import	GetTmcData,ChangeTmcGroup,GetGroupHistory,GetLastStatus
from	forms			import	GroupForm




### --- Перевод в группу ТМЦ ---
def	TmcData6(request):

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
        form = GroupForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            group = form.cleaned_data['group']
            ChangeTmcGroup(GetUserKod(request),tmc_id,comment,group)



    d = GetTmcData(tmc_id)
    data = GetGroupHistory(tmc_id)

    form = GroupForm(None)

    s =GetLastStatus(tmc_id)

    c = RequestContext(request,{'d':d,'form':form,'data':data,'s':s})
    c.update(csrf(request))
    return render_to_response("tmc/tmcdata6.html",c)


