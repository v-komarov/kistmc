#coding:utf-8
import	datetime
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	kis.lib.tmc		import	GetTmcData,GetTmcSpec,NewSpec as NewSpecData,DelSpec,GetTmcSpecData,EditSpec as EditSpecData,AddTmcSpecMulty,GetLastStatus,PullSpec
from	forms			import	SpecFileForm,SpecForm,NumberForm
from kis.lib.tmc import GetSpecStatusList



### --- Данные заявки ТМЦ ---
def	TmcData1(request):


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


    ### --- Затираем строку поиска ---
    request.session['search'] = ''


    if request.method == 'GET':
        try:
            rec_id = request.GET['delete_id']
            DelSpec(GetUserKod(request),rec_id)
        except:
            pass




    if request.method == 'POST':
        nform = NumberForm(request.POST)
        if nform.is_valid():
            n = nform.cleaned_data['n']
            spec = GetTmcSpec('%s' % n)
            PullSpec(GetUserKod(request),tmc_id,spec)

    form = SpecFileForm(None)


    d = GetTmcData(tmc_id)
    data = GetTmcSpec(tmc_id)
    stspec = GetSpecStatusList()

    s = GetLastStatus(tmc_id)

    nform = NumberForm(None)

    c = RequestContext(request,{'d':d,'data':data,'form':form,'s':s,'nform':nform, 'stspec':stspec})
    c.update(csrf(request))
    return render_to_response("tmc/tmcdata1.html",c)







### --- Добавление содержимого ----
def	NewSpec(request):

    """
    if CheckAccess(request,'2') != 'OK':
	return render_to_response("tmc/notaccess/tmc.html")
    """

    try:
        tmc_id = request.session['tmc_id']
    except:
        return HttpResponseRedirect("/tmc")


    if request.method == 'POST':
        form = SpecForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            okei = form.cleaned_data['okei']
            q = form.cleaned_data['q']
            cost = form.cleaned_data['cost']
            analog = form.cleaned_data['analog']
            r = NewSpecData(GetUserKod(request),tmc_id,name,okei,q,cost,analog)
            if r == 'OK':
                return HttpResponseRedirect("/tmcdata")



    form = SpecForm(None)
    form.fields['cost'].initial = '0.00'
    form.fields['q'].initial = '0.00'

    d = GetTmcData(tmc_id)


    c = RequestContext(request,{'form':form,'d':d})
    c.update(csrf(request))
    return render_to_response("tmc/newspec.html",c)





### --- Изменение содержимого ----
def	EditSpec(request):

    """
    if CheckAccess(request,'2') != 'OK':
	return render_to_response("tmc/notaccess/tmc.html")
    """

    try:
        tmc_id = request.session['tmc_id']
    except:
        return HttpResponseRedirect("/tmc")

    try:
        spec_id = request.GET['spec_id']
        request.session['spec_id'] = spec_id
    except:
        pass

    try:
        spec_id = request.session['spec_id']
    except:
        return HttpResponseRedirect("/tmcdata")
	



    if request.method == 'POST':
        form = SpecForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            okei = form.cleaned_data['okei']
            q = form.cleaned_data['q']
            cost = form.cleaned_data['cost']
            analog = form.cleaned_data['analog']
            r = EditSpecData(GetUserKod(request),spec_id,name,okei,q,cost,analog)
            if r == 'OK':
                return HttpResponseRedirect("/tmcdata")

    data = GetTmcSpecData(spec_id)

    form = SpecForm(None)
    form.fields['name'].initial = data[3]
    form.fields['okei'].initial = data[9]
    form.fields['q'].initial = data[5]
    form.fields['cost'].initial = data[6]
    form.fields['analog'].initial = data[7]

    d = GetTmcData(tmc_id)

    c = RequestContext(request,{'form':form,'d':d})
    c.update(csrf(request))
    return render_to_response("tmc/editspec.html",c)

