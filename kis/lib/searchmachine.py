#coding:utf-8
from	django.db	import	connections, transaction
import	xappy


def	CreateIndex():

    connection = xappy.IndexerConnection('kis/lib/data')

    connection.add_field_action('kod', xappy.FieldActions.INDEX_EXACT)
    connection.add_field_action('name', xappy.FieldActions.INDEX_FREETEXT, language='ru')

    connection.close()


def	MakeIndex():

    connection = xappy.IndexerConnection('kis/lib/data')

    cursor = connections['default'].cursor()
    cursor.execute("SELECT rec_id,name FROM t_show_store_eisup_list;")
    data = cursor.fetchall()

    for item in data:
	doc = xappy.UnprocessedDocument()
	doc.fields.append(xappy.Field('kod',item[0].encode('utf-8')))
	doc.fields.append(xappy.Field('name',item[1].encode('utf-8')))
	connection.add(doc)

    connection.flush()
    connection.close()

