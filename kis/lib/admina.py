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




### Список номенклатуры
def	GetRangeList():
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_rec_id,t_name FROM t_tmc_range ORDER BY t_name;")
    data = cursor.fetchall()

    return data




### Список номенклатуры
def	NewRange(name):
    name = name.encode('utf-8')
    cursor = connections['main'].cursor()
    cursor.execute("SELECT t_newtmcrange(%s);",(name,))
    data = cursor.fetchone()

    return data[0]


### Удаление номенклатуры
def DeleteRange(range_id):
    cursor = connections['main'].cursor()
    cursor.execute("DELETE FROM t_tmc_range WHERE t_rec_id=%s;", (range_id,))

    return "OK"
