#coding:utf-8


import json

from django.http import HttpResponse
from kis.lib.userdata import GetUserKod
from kis.lib.tmc import NewSpecStatus, DeleteSpec



def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get



        ### Изменение статуса номенклатуры
        if r.has_key("action") and rg("action") == 'spec_status':
            spec_id = request.GET["spec_id"]
            status_id = int(request.GET["status_id"],10)

            user_id = GetUserKod(request)

            NewSpecStatus(user_id,spec_id,status_id)
            #print spec_id,status_id
            response_data = {'result':'OK'}


        ### Удаление номенклатуры
        if r.has_key("action") and rg("action") == 'spec_delete':
            spec_id = request.GET["spec_id"]
            DeleteSpec(spec_id)
            response_data = {'result':'OK'}




    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
