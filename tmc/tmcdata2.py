#coding:utf-8
import	os.path
import	datetime
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	kis.lib.tmc		import	GetTmcData,AddTmcDoc,GetTmcDocList,GetDoc,DeleteDoc,GetLastStatus
from	forms			import	LoadFile




### --- Документы ---
def	TmcData2(request):

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



    if request.method == 'GET':
	try:
	    rec_id = request.GET['delete_id']
	    DeleteDoc(rec_id)
	except:
	    pass


    if request.method == 'POST':
	form = LoadFile(request.POST)
	if form.is_valid():
	    try:
		comment = form.cleaned_data['comment']
		file_name = request.FILES['file_load'].name
		file_data = request.FILES['file_load'].read()
		file_name = file_name.split('\\')[-1]
		(path,ext) = os.path.splitext(file_name)
		file_name = file_name.replace(' ','_')
		AddTmcDoc(GetUserKod(request),tmc_id,file_name,comment,ext,file_data)
	    except:
		pass


    ### --- Отображение ---
    if request.method == 'GET':
	try:
	    doc_id = request.GET['doc_id']
	    f = GetDoc(doc_id)
	    response = HttpResponse(content_type='application/%s' % f[0][-1:])
	    attach = u'attachment; filename=\"%s\"' % (f[2])
	    response['Content-Disposition'] = attach.encode('utf-8')
	    response.write(f[1])
	    return response
	except:
	    pass



    form = LoadFile(None)


    d = GetTmcData(tmc_id)
    data = GetTmcDocList(tmc_id)

    s = GetLastStatus(tmc_id)

    c = RequestContext(request,{'d':d,'form':form,'data':data,'s':s})
    c.update(csrf(request))
    return render_to_response("tmc/tmcdata2.html",c)




