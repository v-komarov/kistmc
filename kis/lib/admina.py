#coding:utf-8

import datetime
from	django.db	import	connections
import	psycopg2




### Список с доступом ко всем заявкам
def	GetAccessAll():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_d_readall;")
    data = cursor.fetchall()

    return data




### Добавление пользователю в группу
def	AddUserGroup(user_id,group_id):
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_addusergroup(%s,%s);", (user_id,group_id))

    return "OK"



### Список пользователей группы
def	GetUserGroup(group_id):
    cursor = connections['main'].cursor()
    cursor.execute("SELECT * FROM t_show_tmc_user_groups WHERE group_id=%s;", (group_id,))
    data = cursor.fetchall()

    return data



### Удаление пользователя из группы
def DelUserGroup(user_id,group_id):
    cursor = connections['main'].cursor()
    cursor.execute("DELETE FROM t_tmc_user_groups WHERE user_id=%s AND group_id=%s;", (user_id,group_id))

    return "OK"
