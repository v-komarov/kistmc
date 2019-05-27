#coding:utf-8

import	xlwt

from	tmc	import	GetReportSpecData

### --- Отчет  ---
def	ReportSpecData(response,chief,start_date,end_date):


    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Report')

    default_style = xlwt.Style.default_style

    sheet.col(0).width = 256*10
    sheet.col(1).width = 256*10
    sheet.col(2).width = 256*20
    sheet.col(3).width = 256*10
    sheet.col(4).width = 256*50
    sheet.col(5).width = 256*10
    sheet.col(6).width = 256*10
    sheet.col(7).width = 256*30
    sheet.col(8).width = 256*30
    
    style = xlwt.easyxf('font: bold 1')

    sheet.write(0,0,'Дата',style)
    sheet.write(0,1,'Заявка ТМЦ',style)
    sheet.write(0,2,'Статус',style)
    sheet.write(0,3,'№',style)
    sheet.write(0,4,'Наименование',style)
    sheet.write(0,5,'Ед.из.',style)
    sheet.write(0,6,'Кол-во',style)
    sheet.write(0,7,'Руководитель',style)
    sheet.write(0,8,'Инициатор',style)

    data = GetReportSpecData(chief,start_date,end_date)

    i = 1
    for row in data:
	sheet.write(i,0,row[8])
	sheet.write(i,1,row[0])
	sheet.write(i,2,row[3])
	sheet.write(i,3,row[4])
	sheet.write(i,4,row[5])
	sheet.write(i,5,row[6])
	sheet.write(i,6,row[7])
	sheet.write(i,7,row[9]+' '+row[10])
	sheet.write(i,8,row[11]+' '+row[12])
	i = i + 1
    
    


    book.save(response)
    return response


