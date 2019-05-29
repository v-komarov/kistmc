#coding:utf-8
from	django.db	import	connections
from	kis.lib.userdata	import	CheckAccess
import	psycopg2
import	os
import	os.path
import	xlrd


### --- Вспомогательная функция загрузки файлов в базу ---
def	LoadDataFile():
    cursor = connections['main'].cursor()
    file_name = os.listdir('/home/task/tmc')
    for item in file_name:
        try:
            f = open('/home/task/tmc/'+item,'rb')
            data = f.read()
            f.close()
            (path,ext) = os.path.splitext(item)
            path = path.encode("utf-8")
            cursor.execute("SELECT count(*) FROM t_tmc_docs WHERE t_filedata IS NULL AND t_rec_id='%s'" % (path))
            d = cursor.fetchone()
            if d[0] == 1:
                cursor.execute("UPDATE t_tmc_docs SET t_filedata=%s WHERE t_rec_id=%s;", (psycopg2.Binary(data),path))
        except:
            pass



### --- Получение списка заявок ---
def	GetTmcList(search,group,status=''):    
    search = search.encode("utf-8").replace(' ','')
    group = group.encode("utf-8")
    status = status.encode("utf-8")

    cursor = connections['main'].cursor()
    if search == '' and status == '':
        cursor.execute("SELECT * FROM t_show_tmc WHERE grouptmc='%s';" % (group))
    elif search != '' and status == '':
        cursor.execute("""SELECT * FROM t_show_tmc WHERE grouptmc='%s' AND (\
        \
        to_tsvector('russian',rec_id) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',date_create) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',tema) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',status_name) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',user_name1) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',user_name2) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',user_phone) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',ruk_name1) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',ruk_name2) @@ to_tsquery('russian','%s:*')) \
        ;""" % (group,search,search,search,search,search,search,search,search,search))
    elif search == '' and status != '':
        cursor.execute("SELECT * FROM t_show_tmc WHERE grouptmc='%s' AND status_kod='%s';" % (group,status))
    else:
        cursor.execute("""SELECT * FROM t_show_tmc WHERE grouptmc='%s' AND status_kod='%s' AND (\
        \
        to_tsvector('russian',rec_id) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',date_create) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',tema) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',status_name) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',user_name1) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',user_name2) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',user_phone) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',ruk_name1) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',ruk_name2) @@ to_tsquery('russian','%s:*')) \
        ;""" % (group,status,search,search,search,search,search,search,search,search,search))

    data = cursor.fetchall()

    return data




### --- Получение данных по заявке ---
def	GetTmcData(tmc_id):
    tmc_id = tmc_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc WHERE rec_id='%s';" % (tmc_id))
    data = cursor.fetchone()

    return data



### --- Получение данных составки заявки ---
def	GetTmcSpec(tmc_id):
    tmc_id = tmc_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc_spec WHERE tmc_kod='%s';" % (tmc_id))
    data = cursor.fetchall()

    return data




### --- Получение справочника ОКЕИ ---
def	GetOkei():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT rec_id,okei_name FROM t_show_tmc_okei;")
    data = cursor.fetchall()

    return data



### --- Список выбора пользователя ---
def	GetUserList():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_rec_id,t_user_name2||' '||t_user_name1 as name FROM t_user_kis WHERE t_use=true ORDER BY 2;")
    data = cursor.fetchall()

    return data


"""
#### --- Добавление в группу финансы ---
def	AddGroupFinance(user_kod):
    user_kod = user_kod.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT count(*) FROM t_tmc_admin_group WHERE t_user_kod=btrim('%s') AND t_type_kod=0;" % (user_kod))
    data = cursor.fetchone()
    if data[0] == 0:
        cursor = connections['main'].cursor()
        cursor.execute("INSERT INTO t_tmc_admin_group (t_user_kod,t_type_kod) VALUES('%s',0);" % (user_kod))

"""

### --- Получение административных групп ---
def	GetAdminGroupList(type_kod='0'):
    type_kod = type_kod.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc_admin_group WHERE type_kod='%s';" % (type_kod))
    data = cursor.fetchall()

    return data

"""

#### --- Удаление из административной группы ---
def	DelAdminGroup(rec_id):
    rec_id = rec_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("DELETE FROM t_tmc_admin_group WHERE t_rec_id=%s;" % (rec_id))



#### --- Добавление в группу логистика ---
def	AddGroupLogistic(user_kod):
    user_kod = user_kod.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT count(*) FROM t_tmc_admin_group WHERE t_user_kod=btrim('%s') AND t_type_kod=1;" % (user_kod))
    data = cursor.fetchone()
    if data[0] == 0:
        cursor = connections['main'].cursor()
        cursor.execute("INSERT INTO t_tmc_admin_group (t_user_kod,t_type_kod) VALUES('%s',1);" % (user_kod))

"""



### Спроавочник видов проекта
def GetProjectsType():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_rec_id,t_name FROM t_tmc_projects ORDER BY t_name;")
    data = cursor.fetchall()

    return data





#### --- Создание новой заявки ---
def	NewTmc(user_kod,tema,text,group,project,project_num):
    user_kod = user_kod.encode("utf-8")
    tema = tema.encode("utf-8")
    text = text.encode("utf-8")
    group = group.encode("utf-8")
    project_num = project_num.encode("utf-8")
    project = int(project,10)

    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_NewTmc(%s,%s,%s,%s,%s,%s);",[user_kod,tema,text,group,project,project_num])
    data = cursor.fetchone()

    return data[0]



#### --- Создание нового содержимого заявки ---
def	NewSpec(user_kod,tmc_id,name,okei,q,cost,analog):
    user_kod = user_kod.encode("utf-8")
    tmc_id = tmc_id.encode("utf-8")
    name = name.encode("utf-8")
    okei = okei.encode("utf-8")
    q = q.replace(',','.').encode("utf-8")
    cost = cost.replace(',','.').encode("utf-8")
    analog = analog.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_AddTmcSpec('%s',%s,'%s',%s,%s,%s,'%s');" % (user_kod,tmc_id,name,okei,q,cost,analog))
    data = cursor.fetchone()

    return data[0]



#### --- Удаление содержимого заявки ---
def	DelSpec(user_kod,rec_id):
    user_kod = user_kod.encode("utf-8")
    rec_id = rec_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_DelTmcSpec('%s','%s');" % (user_kod,rec_id))
    data = cursor.fetchone()
    return data[0]



### --- Получение записи состава заявки ---
def	GetTmcSpecData(spec_id):
    spec_id = spec_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc_spec WHERE rec_id='%s';" % (spec_id))
    data = cursor.fetchone()

    return data



#### --- Изменение содержимого заявки ---
def	EditSpec(user_kod,rec_id,name,okei,q,cost,analog):
    user_kod = user_kod.encode("utf-8")
    rec_id = rec_id.encode("utf-8")
    name = name.encode("utf-8")
    okei = okei.encode("utf-8")
    q = q.replace(',','.').encode("utf-8")
    cost = cost.replace(',','.').encode("utf-8")
    analog = analog.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_EditTmcSpec('%s','%s','%s',%s,%s,%s,'%s');" % (user_kod,rec_id,name,okei,q,cost,analog))
    data = cursor.fetchone()

    return data[0]



#### --- Добавление содержимого заявки ТМЦ  из файла ---
def AddTmcSpecMulty(user_kod,tmc_id,data):
    user_kod = user_kod.encode("utf-8")
    tmc_id = tmc_id.encode("utf-8")
    rb = xlrd.open_workbook(file_contents=data,formatting_info=True)
    sheet = rb.sheet_by_index(0)

    cursor = connections['main'].cursor()

    for rownum in range(100):
        row = sheet.row_values(rownum)
        row_name = row[0]
        row_okei = '796'
        row_q = row[2]
        cursor.execute("SELECT t_AddTmcSpec('%s',%s,'%s',%s,%s,0,'');" % (user_kod,tmc_id,row_name,row_okei,row_q))



#### --- Прикрепление документа (файла) ---
def	AddTmcDoc(user_kod,tmc_id,filename,comment,fileext,filedata):
    user_kod = user_kod.encode("utf-8")
    tmc_id = tmc_id.encode("utf-8")
    filename = filename.encode("utf-8")
    comment = comment.encode("utf-8")
    fileext = fileext.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_AddTmcDocs(%s,%s,%s,%s,%s,%s);", (user_kod,tmc_id,filename,comment,fileext,psycopg2.Binary(filedata)),)
    data = cursor.fetchone()

    return data[0]



### --- Получение списка приложенных документов ---
def	GetTmcDocList(tmc_id):
    tmc_id = tmc_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc_docs WHERE tmc_kod='%s';" % (tmc_id))
    data = cursor.fetchall()

    return data


### --- Получение файла  ---
def	GetDoc(d_kod):
    d_kod = d_kod.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_ext,t_filedata,t_filename FROM t_tmc_docs WHERE t_rec_id='%s';" % (d_kod))
    data = cursor.fetchone()

    return data



### --- Удаление файла ---
def	DeleteDoc(rec_id):
    rec_id = rec_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("DELETE FROM  t_tmc_docs WHERE t_rec_id='%s';" % (rec_id))



### --- Проверка принадлежности к группе финансов или логистике ---
def	CheckUserGroup(user_id,group_id=0):
    user_id = user_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT count(*) FROM t_tmc_admin_group WHERE t_user_kod='%s' AND t_type_kod=%s;" % (user_id,group_id))
    data = cursor.fetchone()

    if data[0] == 1:
        return 'OK'
    else:
        return 'NONE'



### --- Всех возможных вариантов статусов ---
def	GetStatusListAll():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT rec_id,status_name FROM t_show_tmc_status_choice;")
    data = cursor.fetchall()

    return data



### --- Список статусов в зависимости от статуса заявки ---
def	GetStatusList(status_tmc):
    status_tmc = status_tmc.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT rec_id,status_name FROM t_show_tmc_status_choice WHERE status_tmc='%s';" % (status_tmc))
    data = cursor.fetchall()

    return data



#### --- Установка статуса ---
def	NewTmcStatus(user_kod,tmc_id,comment,status):
    user_kod = user_kod.encode("utf-8")
    tmc_id = tmc_id.encode("utf-8")
    comment = comment.encode("utf-8")
    status = status.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_NewTmcStatus(%s,%s,%s,%s);", [user_kod,tmc_id,comment,status])
    ### --- Финансовая группа ---
    if status == '2' or status == '3' or status == '15':
        if CheckUserGroup(user_kod,group_id=0) == 'OK':
            pass
        else:
            return 'NOTACCESS'
    ### --- Группа логистики ---
    if status == '4' or status == '12':
        if CheckUserGroup(user_kod,group_id=1) == 'OK':
            pass
        else:
            return 'NOTACCESS'
    data = cursor.fetchone()

    return data[0]



### --- Получение истории статусов заявки ---
def	GetStatusHistory(tmc_id):
    tmc_id = tmc_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc_status_history WHERE tmc_kod='%s';" % (tmc_id))
    data = cursor.fetchall()

    return data



### --- Регистрация истории отправки email уведомлений ---
def	EmailHistory(tmc_kod,email,subject):
    tmc_kod = tmc_kod.encode("utf-8")
    email = email.encode("utf-8")
    subject = subject.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("INSERT INTO t_tmc_email_history(t_tmc_kod,t_email,t_subject) VALUES(%s,'%s','%s');" % (tmc_kod,email,subject))



### --- Получение истории email уведомлений ---
def	GetEmailHistory(tmc_id):
    tmc_id = tmc_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc_email_history WHERE tmc_kod='%s';" % (tmc_id))
    data = cursor.fetchall()

    return data


### --- Список email руководителей ---
def	GetEmailRukList():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_email,t_user_name2||' '||t_user_name1 FROM  t_user_kis WHERE t_email IS NOT NULL AND t_email != '' AND t_use=true ORDER BY t_user_name2;")
    data = cursor.fetchall()

    return data


#### --- Изменение группы ТМЦ ---
def	ChangeTmcGroup(user_kod,tmc_id,comment,group):
    user_kod = user_kod.encode("utf-8")
    tmc_id = tmc_id.encode("utf-8")
    comment = comment.encode("utf-8")
    group = group.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_ChangeTmcGroup('%s',%s,'%s','%s');" % (user_kod,tmc_id,comment,group))
    data = cursor.fetchone()

    return data[0]



### --- Получение истории изменения группы ТМЦ ---
def	GetGroupHistory(tmc_id):
    tmc_id = tmc_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc_grouptmc_history WHERE tmc_kod='%s';" % (tmc_id))
    data = cursor.fetchall()

    return data



### --- Список статусов для фильтра ---
def	GetStatusListFilter():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT rec_id,status_name FROM t_show_tmc_status_list;")
    data = cursor.fetchall()

    return data



### --- Регистрация истории отправки email уведомлений ---
def	SetShifr(tmc_kod,author_kod,user_kod,shifr):
    tmc_kod = tmc_kod.encode("utf-8")
    author_kod = author_kod.encode("utf-8")
    user_kod = user_kod.encode("utf-8")
    shifr = shifr.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("UPDATE t_tmc SET t_shifr=btrim('%s') WHERE t_rec_id=%s;" % (shifr,tmc_kod))
    if user_kod == author_kod or CheckUserGroup(user_kod,group_id=0) == 'OK':
        pass


### --- Информация о последнем статусе или комментарии ---
def	GetLastStatus(tmc_id):
    data = GetStatusHistory(tmc_id)
    if len(data) != 0:
        a = data[0]
        return a
    else:
        return ('','','','','','','','','','','','')



### --- Изменение  заявки ТМЦ ---
def	EditTmc(tmc_kod,tema,text,project,project_num):
    tmc_kod = tmc_kod.encode("utf-8")
    tema = tema.encode("utf-8")
    text = text.encode("utf-8")
    project_num = project_num.encode("utf-8")
    project = int(project,10)

    cursor = connections['main'].cursor()
    cursor.execute("UPDATE t_tmc SET t_tema=btrim('%s'), t_note_text=btrim('%s'), t_project=%s, t_project_num=btrim('%s') WHERE t_rec_id=%s AND t_status_kod=0;" % (tema,text,project,project_num,tmc_kod))

    return 'OK'



#### --- Наполнение содержимого заявки на основе другой заявки ---
def PullSpec(user_kod,tmc_id,data):
    user_kod = user_kod.encode("utf-8")
    tmc_id = tmc_id.encode("utf-8")

    cursor = connections['main'].cursor()

    for row in data:
        cursor.execute("SELECT t_AddTmcSpec(%s,%s,%s,%s,%s,%s,%s);" , [user_kod,tmc_id,row[3],row[9],row[5],row[6],row[7]])




### --- Получение списка заявок для внутреннего заказа ---
def	GetTmcOrder():    

    cursor = connections['main'].cursor()
    cursor.execute("SELECT rec_id,'№ '||rec_id||' от '||date_create||' тема: '||substr(tema,1,30) FROM t_show_tmc WHERE status_kod='10' OR status_kod='11';")
    data = cursor.fetchall()

    return data



### --- Создание нового внутреннего заказа ---
def	NewOrder(tmc_kod,project,user_kod,executor_kod):
    tmc_kod = tmc_kod.encode("utf-8")
    project = project.encode("utf-8")
    user_kod = user_kod.encode("utf-8")
    executor_kod = executor_kod.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_NewOrder(%s,%s,%s,%s)",[tmc_kod,project,user_kod,executor_kod])
    data = cursor.fetchone()

    return data[0]



### --- Получение списка внутренних заказов ---
def	GetOrderList(search):    
    search = search.encode("utf-8")
    cursor = connections['main'].cursor()
    if search == '':
        cursor.execute("SELECT * FROM t_show_order;")
    else:
        cursor.execute("""SELECT * FROM t_show_order WHERE \
        \
        to_tsvector('russian',rec_id) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',order_date) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',tmc) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',tmc_date) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',tmc_tema) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',project_name) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',author_name1) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',author_name2) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',author_phone) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',executor_name1) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',executor_name2) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',executor_phone) @@ to_tsquery('russian','%s:*') \
        ;""" % (search,search,search,search,search,search,search,search,search,search,search,search))

    data = cursor.fetchall()

    return data



### --- Получение данных по внутреннему заказу ---
def	GetOrder(rec_id):    
    rec_id = rec_id.encode("utf-8")

    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_order WHERE rec_id=%s;",[rec_id,])
    data = cursor.fetchone()

    return data



### --- Получение состава внутреннего заказа ---
def	GetOrderSpec(order_id):    
    order_id = order_id.encode("utf-8")

    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_order_spec WHERE order_kod=%s;",[order_id,])
    data = cursor.fetchall()

    return data



### --- Сохранение количества в составе ---
def	OrderSetQ(user_kod,spec_id,q):
    user_kod = user_kod.encode("utf-8")
    spec_id = spec_id.encode("utf-8")
    q = q.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_OrderSetQ(%s,%s,%s)",[user_kod,spec_id,q])
    data = cursor.fetchone()

    return data[0]



### --- Получение состава внутреннего заказа ---
def	GetTmcGroupList():    

    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_tmc_group_list;")
    data = cursor.fetchall()

    return data



#### --- Добавление в email рассылку по группе ---
def	AddGroupEmail(user_kod,type_group,tmc_group):
    user_kod = user_kod.encode("utf-8")
    tmc_group = tmc_group.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT count(*) FROM t_tmc_email_group WHERE t_user_kod=btrim(%s) AND t_type_kod=%s AND t_group_tmc=%s;", [user_kod,type_group,tmc_group])
    data = cursor.fetchone()
    if data[0] == 0:
        cursor = connections['main'].cursor()
        cursor.execute("INSERT INTO t_tmc_email_group (t_user_kod,t_type_kod,t_group_tmc) VALUES(%s,%s,%s);", [user_kod,type_group,tmc_group])



### --- Получение списка email рассылки по группам ---
def	GetGroupEmailList(type_kod,grouptmc=''):    

    grouptmc = grouptmc.encode("utf-8")
    cursor = connections['main'].cursor()
    if grouptmc == '':
        cursor.execute("SELECT * FROM t_show_tmc_email_group WHERE type_kod=%s;" , [type_kod])
    else:
        cursor.execute("SELECT * FROM t_show_tmc_email_group WHERE type_kod=%s AND group_kod=%s;" , [type_kod,grouptmc])
        data = cursor.fetchall()

        return data



#### --- Удаление из группы email рассылки ---
def	DelEmailGroup(rec_id):
    rec_id = rec_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("DELETE FROM t_tmc_email_group WHERE t_rec_id=%s;" % (rec_id))




### --- Данные для отчета ReportSpec ---
def	GetReportSpecData(chief,start_date,end_date):

    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc_reportspec WHERE ruk_kod=%s AND tmc_date>=%s AND tmc_date<=%s;" , [chief,start_date,end_date])    
    data = cursor.fetchall()

    return data



### --- Справочник статусов для элементов номенклатуры ---
def GetSpecStatusList():

    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_rec_id,t_name FROM t_tmc_spec_status_list ORDER BY t_name;")
    data = cursor.fetchall()

    return data


### --- Установка статуса номенклатуры ---
def NewSpecStatus(user_id,spec_id,status_id):
    user_id = user_id.encode("utf-8")
    spec_id = spec_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_newspecstatus(%s,%s,%s);", [user_id,spec_id,status_id])
    return 'OK'



### --- Удаление номенклатуры из заявки ---
def DeleteSpec(spec_id):
    spec_id = spec_id.encode("utf-8")
    cursor = connections['main'].cursor()
    cursor.execute("UPDATE t_tmc_spec SET t_rec_delete=1 WHERE t_rec_id=%s;", [spec_id,])
    return 'OK'





### --- Получение номенклатуры по проектам ---
def	GetSpectProj(search,project,status):
    search = search.encode("utf-8").replace(' ','')
    project = 0 if project == '' else int(project,10)
    status = 0 if status == '' else int(status,10)

    cursor = connections['main'].cursor()
    if search == '':
        cursor.execute("SELECT * FROM t_show_tmc_spec_project WHERE project_id=%s AND status_id=%s;", (project,status))
    else:
        cursor.execute("""SELECT * FROM t_show_tmc_spec_project WHERE project_id=%s AND status_id=%s AND (\
        \
        to_tsvector('russian',project_num) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',tema) @@ to_tsquery('russian','%s:*') OR \
        to_tsvector('russian',row_name) @@ to_tsquery('russian','%s:*')) \
        ;""" % (project,status,search,search,search))

    data = cursor.fetchall()

    return data
