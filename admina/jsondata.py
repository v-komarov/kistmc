#coding:utf-8


import json

from django.http import HttpResponse
from kis.lib.userdata import GetUserKod, AccessAdmin
from kis.lib.tmc import NewSpecStatus, DeleteSpec
from kis.lib.admina import NewRange, DeleteRange



def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get



        ### Добавление номенклатуры
        if r.has_key("action") and rg("action") == 'new_range':
            name = request.GET["name"]
            if AccessAdmin(request) == "OK":
                range_id  = NewRange(name)
                if len(range_id) == 24:
                    response_data = {'result':'OK', 'range_id':range_id}
                else:
                    response_data = {'result': 'error'}
            else:
                response_data = {'result': 'error'}


        ### Удаление номенклатуры
        if r.has_key("action") and rg("action") == 'range_delete':
            range_id = request.GET["range_id"]
            if AccessAdmin(request) == "OK":
                if DeleteRange(range_id) == 'OK':
                    response_data = {'result':'OK'}
                else:
                    response_data = {'result':'error'}
            else:
                response_data = {'result':'error'}





    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
