#coding:utf-8


from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	reportlab.pdfgen	import	canvas
from	reportlab.lib.units	import	mm
from	reportlab.pdfbase	import	pdfmetrics
from	reportlab.pdfbase	import	ttfonts
from	reportlab.lib		import	colors
from	reportlab.lib.pagesizes	import	letter, A4, landscape

from	reportlab.platypus.tables	import	Table, TableStyle
from	reportlab.platypus.doctemplate	import	SimpleDocTemplate
from	reportlab.platypus.paragraph	import	Paragraph
from	reportlab.lib.styles		import	ParagraphStyle,getSampleStyleSheet
from	reportlab.platypus		import	Frame,Spacer

from	reportlab.platypus		import	Image

from	jsondata	import	JsonUser
from	tmc		import	GetOrder,GetOrderSpec



### --- Печастная форма внутреннего заказа ---
def	PrintForm(buff,order_id):

    #### --- Получение даных по заказу ---
    order = GetOrder(order_id)

    ### --- Руководитель ---
    chief = JsonUser(order[7])

    ### --- Исполнитель ---
    user = JsonUser(order[8])

    ### --- Получатель ---
    executer = JsonUser(order[9])


    #### --- Получение состава заказа ---
    spec = GetOrderSpec(order_id)


    Font1 = ttfonts.TTFont('PT','kis/fonts/PTC55F.ttf')
    Font2 = ttfonts.TTFont('PTB','kis/fonts/PTC75F.ttf')
    Font3 = ttfonts.TTFont('PTI','kis/fonts/PTS56F.ttf')


    pdfmetrics.registerFont(Font1)
    pdfmetrics.registerFont(Font2)
    pdfmetrics.registerFont(Font3)


    style = getSampleStyleSheet()
    style.add(ParagraphStyle(name='MyStyle',wordWrap=True,fontName='PTB',fontSize=10,spaceAfter=5*mm,spaceBefore=20*mm,alignment=0))
    style.add(ParagraphStyle(name='MyStyle0',wordWrap=True,fontName='PT',fontSize=10,spaceAfter=5*mm,spaceBefore=5*mm,alignment=0))
    style.add(ParagraphStyle(name='MyStyle2',wordWrap=True,fontName='PT',fontSize=10,spaceAfter=1*mm,spaceBefore=1*mm,alignment=0))
    
    doc = SimpleDocTemplate(buff,topMargin=10*mm,bottomMargin=10*mm,leftMargin=20*mm,rightMargin=10*mm)



    data = [['№\nпп','Наименование\nматериалов','Ед.\nизм.','Коли-\nчество','Примечание'],
	    ['1','2','3','4','5'],
	    ]
    n = 1
    for item in spec:
	data.append([n,Paragraph(item[2],style["MyStyle2"]),item[3],item[4],''])
	n = n + 1



    t=Table(data,colWidths=[10*mm,90*mm,20*mm,20*mm,40*mm])
    t.setStyle([('FONTNAME',(0,0),(-1,1),'PTB'),
		('FONTSIZE',(0,0),(-1,-1),10),
		('ALIGN',(0,0),(-1,1),'CENTER'),
		('VALIGN',(0,0),(-1,1),'MIDDLE'),
		('ALIGN',(0,2),(-1,-1),'LEFT'),
		('FONTNAME',(0,2),(-1,-1),'PT'),
		('VALIGN',(0,2),(-1,-1),'TOP'),
		('GRID',(0,0),(-1,-1),0.25,colors.black),
		])

    Tdata = [['','Номер\nдокумента','Дата\nсоставления'],
	    ['ВНУТРЕННИЙ ЗАКАЗ',order[0],order[1]]]


    TableHead=Table(Tdata)
    TableHead.setStyle([('FONTNAME',(0,0),(-1,-1),'PTB'),
		('FONTSIZE',(0,0),(-1,-1),10),
		('ALIGN',(0,0),(-1,-1),'CENTER'),
		('VALIGN',(0,0),(-1,-1),'MIDDLE'),
		('GRID',(1,0),(-1,-1),0.25,colors.black),
		])


    elements = []
    

    elements.append(TableHead)
    elements.append(Paragraph('Организация: ЗАО "СибТрансТелеКом"',style["MyStyle"]))
    elements.append(Paragraph('Структурное подразделение-получатель: %s' % executer.j['department'].encode("utf-8"),style["MyStyle0"]))
    elements.append(Paragraph('Проект : %s' % order[6].encode("utf-8"),style["MyStyle0"]))
    elements.append(Paragraph('Номер заявки : %s от %s' % (order[2].encode("utf-8"),order[3].encode("utf-8")),style["MyStyle0"]))
    elements.append(Paragraph('Шифр затрат : %s' % order[5].encode("utf-8"),style["MyStyle0"]))
    elements.append(t)
    elements.append(Paragraph('Затребовал руководитель подразделения : %s %s.%s.' % (chief.j['name1'].encode("utf-8"),chief.j['name2'][:1].encode("utf-8"),chief.j['name3'][:1].encode("utf-8")),style["MyStyle0"]))
    elements.append(Paragraph('Исполнитель: %s %s.%s.' % (user.j['name1'].encode("utf-8"),user.j['name2'][:1].encode("utf-8"),user.j['name3'][:1].encode("utf-8")),style["MyStyle0"]))
    elements.append(Paragraph('Получатель должность: %s' % executer.j['job'].encode("utf-8"),style["MyStyle0"]))
    elements.append(Paragraph('Получатель подпись:__________________ расшифровка подписи: %s %s.%s.' % (executer.j['name1'].encode("utf-8"),executer.j['name2'][:1].encode("utf-8"),executer.j['name3'][:1].encode("utf-8")),style["MyStyle0"]))
    
    doc.build(elements)

    return buff
