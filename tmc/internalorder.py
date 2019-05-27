#coding:utf-8
import	datetime
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	SearchOrderForm,OrderForm
from	kis.lib.tmc		import	GetTmcList,NewOrder,GetOrderList,GetOrder,GetOrderSpec,OrderSetQ

from	cStringIO	import	StringIO

from	kis.lib.tmc_print	import	PrintForm





### --- Внутренний заказ ---
def	List(request):


    try:
	if CheckAccess(request,'2') != 'OK':
	    return render_to_response("tmc/notaccess/tmc.html")
    except:
	return HttpResponseRedirect('/')



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
    except:
	search = ''



    if request.method == 'POST':
	
	form = SearchOrderForm(request.POST)
	if form.is_valid():
	    search = form.cleaned_data['search']
	    request.session['search'] = search



    data = GetOrderList(search)


    form = SearchOrderForm(None)
    form.fields['search'].initial = search



    paginator = Paginator(data,50)
    try:
	data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
	data_page = paginator.page(paginator.num_pages)


    c = RequestContext(request,{'form':form,'data':data_page})
    c.update(csrf(request))
    return render_to_response("tmc/orderlist.html",c)









### --- Новый внутренний заказ ---
def	New(request):


    try:
	if CheckAccess(request,'2') != 'OK':
	    return render_to_response("tmc/notaccess/tmc.html")
    except:
	return HttpResponseRedirect('/')





    if request.method == 'POST':
	
	form = OrderForm(request.POST)
	if form.is_valid():
	    tmc = form.cleaned_data['tmc']
	    project = form.cleaned_data['project']
	    executor = form.cleaned_data['executor']
	    r = NewOrder(tmc,project,GetUserKod(request),executor)
	    if r == 'OK':
		return HttpResponseRedirect('/tmcorderlist')
		

    form = OrderForm(None)

    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("tmc/ordernew.html",c)









### --- Изменение состава ---
def	Spec(request):


    try:
	if CheckAccess(request,'2') != 'OK':
	    return render_to_response("tmc/notaccess/tmc.html")
    except:
	return HttpResponseRedirect('/')


    if request.method == 'GET':
	try:
	    order_id = request.GET['order_id']
	    request.session['order_id'] = order_id
	except:
	    pass

    ### --- Восстановление номера заказа ---
    try:
	order_id = request.session['order_id']
    except:
	return HttpResponseRedirect('/tmcorderlist')
	



    if request.method == 'POST':
	data = GetOrderSpec(order_id)
	for item in data:
	    try:
		name = 'spec'+item[0]
		q = request.POST[name]
		OrderSetQ(GetUserKod(request),item[0],q)
	    except:
		pass



    ### --- Данные по составу ---
    data = GetOrderSpec(order_id)

    ### --- Данные по заказу --
    order = GetOrder(order_id)

    c = RequestContext(request,{'data':data,'order':order})
    c.update(csrf(request))
    return render_to_response("tmc/orderspec.html",c)









### --- Печатная форма ---
def	OrderPrint(request):

	order_id = request.GET['order_id']

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="order.pdf"'
	buff = StringIO()
	result = PrintForm(buff,order_id)
	response.write(result.getvalue())
	buff.close()
	return response

