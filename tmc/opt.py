#coding:utf-8
import	datetime
from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	kis.lib.userdata	import	CheckAccess,GetUserKod
from	forms			import	UserChoiceForm,GroupEmailForm
from	kis.lib.tmc		import	AddGroupFinance,GetAdminGroupList,DelAdminGroup,AddGroupLogistic,AddGroupEmail,GetGroupEmailList,DelEmailGroup




### --- Настройки Финансовая группа ---
def	Finance(request):


    if CheckAccess(request,'16') != 'OK':
	return render_to_response("tmc/notaccess/opt.html")



    if request.method == 'POST':
	
	form = UserChoiceForm(request.POST)
	if form.is_valid():
	    user = form.cleaned_data['user']
	    if len(user)>7:
		AddGroupFinance(user)

    if request.method == 'POST':
	
	form2 = GroupEmailForm(request.POST)
	if form2.is_valid():
	    user_kod = form2.cleaned_data['user_kod']
	    group = form2.cleaned_data['group']
	    AddGroupEmail(user_kod,0,group)



    if request.method == 'GET':
	try:
	    rec_id = request.GET['delete_id']
	    DelAdminGroup(rec_id)
	except:
	    pass


    if request.method == 'GET':
	try:
	    rec_id = request.GET['email_group']
	    DelEmailGroup(rec_id)
	except:
	    pass


    form = UserChoiceForm(None)
    form2 = GroupEmailForm(None)

    data = GetAdminGroupList()
    data2 = GetGroupEmailList(0)

    form.fields['user'].initial = ''
    form2.fields['user_kod'].initial = ''


    c = RequestContext(request,{'form':form,'data':data,'form2':form2,'data2':data2})
    c.update(csrf(request))
    return render_to_response("tmc/finance.html",c)





### --- Настройки группа логистики ---
def	Logistic(request):


    if CheckAccess(request,'16') != 'OK':
	return render_to_response("tmc/notaccess/opt.html")



    if request.method == 'POST':
	
	form = UserChoiceForm(request.POST)
	if form.is_valid():
	    user = form.cleaned_data['user']
	    if len(user)>7:
		AddGroupLogistic(user)


    if request.method == 'POST':
	
	form2 = GroupEmailForm(request.POST)
	if form2.is_valid():
	    user_kod = form2.cleaned_data['user_kod']
	    group = form2.cleaned_data['group']
	    AddGroupEmail(user_kod,1,group)



    if request.method == 'GET':
	try:
	    rec_id = request.GET['delete_id']
	    DelAdminGroup(rec_id)
	except:
	    pass


    if request.method == 'GET':
	try:
	    rec_id = request.GET['email_group']
	    DelEmailGroup(rec_id)
	except:
	    pass



    form = UserChoiceForm(None)
    form2 = GroupEmailForm(None)


    data = GetAdminGroupList(type_kod='1')
    data2 = GetGroupEmailList(1)

    form.fields['user'].initial = ''
    form2.fields['user_kod'].initial = ''


    c = RequestContext(request,{'form':form,'data':data,'form2':form2,'data2':data2})
    c.update(csrf(request))
    return render_to_response("tmc/logistic.html",c)


