#coding:utf-8

from	django.http	import	HttpResponse

from	django.db		import	connections, transaction
from	django.core.mail	import	send_mail
from	kis.lib.tmc		import	GetTmcData,GetTmcSpec




### вывод информации по заявке ТМЦ в формате csv
def GetCsvData(request):

    tmc_id = request.session['tmc_id']

    tmc = GetTmcData(tmc_id)
    tmcspec = GetTmcSpec(tmc_id)

    
    response_data = u""
    response_data = response_data + u";Заявка ТМС номер {num} от {date};;;;;;\n".format(num=tmc[0],date=tmc[2])
    response_data = response_data + u";Текстовое описание: {text};;;;;;\n".format(text=tmc[4])
    response_data = response_data + u";Тема: {tema};;;;;;\n".format(tema=tmc[3])
    response_data = response_data + u";Статус: {status};;;;;;\n".format(status=tmc[6])
    response_data = response_data + u";Исполнитель (телефон): {worker1} {worker2} ({phone});;;;;;\n".format(worker1=tmc[10],worker2=tmc[9],phone=tmc[12])
    response_data = response_data + u";Руководитель: {chif1} {chif2};;;;;;\n".format(chif1=tmc[17],chif2=tmc[16])

    response_data = response_data + u";;;;;;;\n;;;;;;;\n"

    response_data = response_data + u";Состав заявки;;;;;;\n"
    response_data = response_data + u"№пп;Наименование;Ед.из.;Кол-во;Цена;Аналог;;\n"

    for row in tmcspec:
	response_data = response_data + u"{n};{name};{ed};{cou};{price};{analog};;\n".format(n=row[2],name=row[3],ed=row[4],cou=row[5],price=row[6],analog=row[7])


    response_data = response_data.encode('cp1251')


    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="tmc%s.csv"' % tmc[0]
    response.write(response_data)
    return response
