#coding:utf-8

from django.db import connections
from django.core.mail import send_mail
from kis.lib.tmc import GetTmcData,GetAdminGroupList,GetStatusHistory,EmailHistory,GetGroupEmailList
from django.core.mail import EmailMessage


kisurl = "http://10.6.3.54:8060"


### --- Отправка запроса подписи ---
def Email2Ruk(email,tmc_id):

    ### --- Получение данных по заявке ---
    d = GetTmcData(tmc_id)

    tmc_txt = d[4]
    author = d[13]

    ### --- Кому отправляем ---
    address = []
    address.append(email)

    m = u"""
    <p>
    Прошу подписать Заявку ТМЦ № {tmc} <a href="{kisurl}/tmcdata/?tmc_id={tmc}">Ссылка</a><br><br>
    {txt}<br>
    </p>
    """.format(kisurl=kisurl,tmc=d[0],txt=tmc_txt)

    subj = 'KIS-messager'
    
    em = EmailMessage(
        subject = subj,
        body = m,
        from_email = author,
        to = address
    )
    
    em.content_subtype = "html"
    em.send()



    ### -- Собираем отправку в лог ---
    EmailHistory(tmc_id,email,u'Запрос на подпись руководителя')






#### --- Рассылка уведомлений по статусу заявки ---
def EmailStatusInfo(tmc_id):
    ### --- Получение данных по заявке ---
    d = GetTmcData(tmc_id)
    ### --- Данные по установленному статусу ---
    s_last = GetStatusHistory(tmc_id)[0]

    ### --- Группа ТМЦ ---
    tmcgroup = d[1]

    author = s_last[10]
    status_tmc = s_last[3]
    comment = s_last[8]

    tmc_txt = d[4]
    
    ### --- Кому отправляем ---
    mail = []
    mail.append(d[13])

    ### --- Для групп финасы и логистика дополнительная рассылка ---
    ### --- Группа финансы ---
    if s_last[11] == '1' or s_last[11] == '8' or s_last[11] == '9' or s_last[11] == '13' or s_last[11] == '16':
        group = GetGroupEmailList(0,tmcgroup)
        for item in group:
            mail.append(item[5])

    ### --- Группа логистика ---
    if s_last[11] == '3' or s_last[11] == '10' or s_last[11] == '9' or s_last[11] == '13' or s_last[11] == '15' or s_last[11] == '16':
        group = GetGroupEmailList(0,tmcgroup)
        for item in group:
            mail.append(item[5])


    for address in mail:

        m = u"""
        <p>
        Уведомление о статусе (Заявки ТМЦ)<br><br>
        Заявка № {tmc} <a href="{kisurl}/tmcdata/?tmc_id={tmc}">Ссылка</a><br>
        {txt}<br>
        Статус: {status}<br>
        Комментарий: {comment}<br>
        """.format(kisurl=kisurl,tmc=d[0],txt=tmc_txt,status=status_tmc,comment=comment)

        subj = 'KIS-messager'
    
        em = EmailMessage(
            subject = subj,
            body = m,
            from_email = author,
            to = [address,]
        )
    
        em.content_subtype = "html"
        em.send()


        EmailHistory(tmc_id,address,u'Уведомление о статусе: '+status_tmc)


