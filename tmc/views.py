#coding:utf-8
import	datetime
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	SearchForm,NewTmcForm,EditTmcForm, SearchSpecForm
from	kis.lib.tmc		import	GetTmcList,NewTmc,GetTmcData,GetTmcSpec,EditTmc, GetSpectProj



### --- Заявки ТМЦ ---
def	ListTmc(request):


    ### --- Получение номера страницы ---
    try:
        page = int(request.GET.get('page',1))
        request.session['page'] = page
    except:
        pass
	
    try:
        page = int(request.session['page'])
    except:
        page = 1



    try:
        search = request.session['search']
        status = request.session['status']
        group = request.session['group']
    except:
        search = ''
        status = ''
        group = ''



    if request.method == 'POST':
	
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            status = form.cleaned_data['status']
            group = form.cleaned_data['group']
            request.session['search'] = search
            request.session['status'] = status
            request.session['group'] = group


    data = GetTmcList(search,group,status)


    form = SearchForm(None)
    form.fields['search'].initial = search
    form.fields['status'].initial = status
    form.fields['group'].initial = group



    paginator = Paginator(data,50)
    try:
        data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data_page = paginator.page(paginator.num_pages)


    c = RequestContext(request,{'form':form,'data':data_page})
    c.update(csrf(request))
    return render_to_response("tmc/tmc.html",c)





### --- Новая заявка ---
def	TmcNew(request):


    if request.method == 'POST':
	
        form = NewTmcForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            tema = form.cleaned_data['tema']
            text = form.cleaned_data['text']
            project = form.cleaned_data['project']
            project_num = form.cleaned_data['project_num']
            r = NewTmc(GetUserKod(request),tema,text,group,project,project_num)
            if r == 'OK':
                return HttpResponseRedirect("/tmc")


    form = NewTmcForm(None)


    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("tmc/tmcnew.html",c)






### --- Редактирование содержимого заявки ---
def	TmcEdit(request):

    """
    if CheckAccess(request,'2') != 'OK':
	return render_to_response("tmc/notaccess/tmc.html")
    """

    try:
        tmc_id = request.session['tmc_id']
    except:
        return HttpResponseRedirect("/tmc")


    if request.method == 'POST':
	
        form = EditTmcForm(request.POST)
        if form.is_valid():
            tema = form.cleaned_data['tema']
            text = form.cleaned_data['text']
            project = form.cleaned_data['project']
            project_num = form.cleaned_data['project_num']
            r = EditTmc(tmc_id,tema,text,project,project_num)
            if r == 'OK':
                return HttpResponseRedirect("/tmcdata")
		


    d = GetTmcData(tmc_id)
    data = GetTmcSpec(tmc_id)

    form = EditTmcForm(None)
    form.fields['tema'].initial = d[3]
    form.fields['text'].initial = d[4]
    form.fields['project'].initial = "%s" % d[26]
    form.fields['project_num'].initial = d[25]




    c = RequestContext(request,{'d':d,'form':form,'data':data})
    c.update(csrf(request))
    return render_to_response("tmc/tmcedit.html",c)


### --- Материалы проектов ---
def ProjSpec(request):
    ### --- Получение номера страницы ---
    try:
        page = int(request.GET.get('page', 1))
        request.session['page'] = page
    except:
        pass

    try:
        page = int(request.session['page'])
    except:
        page = 1

    try:
        search = request.session['search']
        status = request.session['status']
        project = request.session['project']
    except:
        search = ''
        status = ''
        project = ''

    if request.method == 'POST':

        form = SearchSpecForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            status = form.cleaned_data['status']
            project = form.cleaned_data['project']
            request.session['search'] = search
            request.session['status'] = status
            request.session['project'] = project

    data = GetSpectProj(search, project, status)

    form = SearchSpecForm(None)
    form.fields['search'].initial = search
    form.fields['status'].initial = status
    form.fields['project'].initial = project

    paginator = Paginator(data, 50)
    try:
        data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data_page = paginator.page(paginator.num_pages)


    c = RequestContext(request, {'form': form, 'data': data_page})
    c.update(csrf(request))
    return render_to_response("tmc/proj.html", c)

