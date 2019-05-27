#coding:utf-8


from django.shortcuts import render

from django.shortcuts import render
from django.template import Context, loader, RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect


from kis.lib.userdata import AccessAdmin
from admina.forms import UserForm
from kis.lib.admina import AddUserGroup, GetUserGroup, DelUserGroup as DelUser





### Состав группы МТС
def MTSGroup(request):



    ### --- Проверка доступа к этой закладки ---
    if AccessAdmin(request) != 'OK':
        c = RequestContext(request,{})
        return render_to_response("admina/notaccess.html",c)


    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            AddUserGroup(user_id,'mts')


    data = GetUserGroup('mts')
    form = UserForm()
    c = RequestContext(request,{'data':data, 'form': form})
    c.update(csrf(request))
    return render_to_response("admina/mtsgroup.html",c)




### Состав группы Финансового контроля
def FinGroup(request):



    ### --- Проверка доступа к этой закладки ---
    if AccessAdmin(request) != 'OK':
        c = RequestContext(request,{})
        return render_to_response("admina/notaccess.html",c)


    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            AddUserGroup(user_id,'fin')


    data = GetUserGroup('fin')
    form = UserForm()
    c = RequestContext(request,{'data':data, 'form': form})
    c.update(csrf(request))
    return render_to_response("admina/fingroup.html",c)




### Удаление пользователя из группы
def DelUserGroup(request):


    ### --- Проверка доступа к этой закладки ---
    if AccessAdmin(request) != 'OK':
        c = RequestContext(request,{})
        return render_to_response("admina/notaccess.html",c)

    user_id = request.GET['user_id']
    group_id = request.GET['group_id']


    DelUser(user_id,group_id)

    if group_id == 'mts':
        return HttpResponseRedirect('/admina/mtsgroup')
    else:
        return HttpResponseRedirect('/admina/fingroup')
