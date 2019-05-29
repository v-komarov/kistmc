#coding:utf-8
import	datetime
from	django	import	forms
from	django.forms.extras.widgets	import	SelectDateWidget

from	kis.lib.tmc	import	GetOkei
from	kis.lib.tmc	import	GetUserList,GetStatusListAll,GetEmailRukList,GetStatusListFilter,GetTmcOrder,GetTmcGroupList, GetProjectsType
from kis.lib.tmc import GetSpecStatusList


tmcgroup = GetTmcGroupList()
tmcgroup.insert(0,('',''))

user_list = GetUserList()
user_list.insert(0,('',''))


### --- Поиск ---
class	SearchForm(forms.Form):
    group = forms.ChoiceField(label='Группа',choices=GetStatusListFilter(),required=False)
    status = forms.ChoiceField(label='Статус',choices=GetStatusListFilter(),required=False)
    search = forms.CharField(label='Строка поиска',required=False)
    def	__init__(self,*args,**kwargs):
        super(SearchForm,self).__init__(*args,**kwargs)
        self.fields['group'].choices = GetTmcGroupList()
        self.fields['status'].choices = GetStatusListFilter()



### --- Поиск по материалам проектов---
class	SearchSpecForm(forms.Form):
    project = forms.ChoiceField(label='Проект',choices=GetStatusListFilter(),required=False)
    status = forms.ChoiceField(label='Статус',choices=GetStatusListFilter(),required=False)
    search = forms.CharField(label='Строка поиска',required=False)
    def	__init__(self,*args,**kwargs):
        super(SearchSpecForm,self).__init__(*args,**kwargs)
        self.fields['project'].choices = GetProjectsType()
        self.fields['status'].choices = GetSpecStatusList()




class	SpecFileForm(forms.Form):
    file_load = forms.FileField(label='Загрузить из файла excel',widget=forms.FileInput,required=False)


### --- Форма для создания новой заяви ТМЦ ---
class	NewTmcForm(forms.Form):
    group = forms.ChoiceField(label='Группа*',required=False)
    tema = forms.CharField(label='Тема*',widget=forms.TextInput(attrs={'class':'g-5',}))
    text = forms.CharField(label='Текст заявки*',widget=forms.Textarea(attrs={'class':'g-5',}))
    project = forms.ChoiceField(label='Проект*', required=False)
    project_num = forms.CharField(label='Номер проекта',widget=forms.TextInput(attrs={'class':'g-5',}), required=False)
    def	__init__(self,*args,**kwargs):
        super(NewTmcForm,self).__init__(*args,**kwargs)
        self.fields['group'].choices = GetTmcGroupList()
        self.fields['project'].choices = GetProjectsType()



class	SpecForm(forms.Form):
    name = forms.CharField(label='Наименование, марка*',widget=forms.TextInput(attrs={'class':'g-5',}))
    okei = forms.ChoiceField(label='Ед.измерения*',choices=GetOkei())
    q = forms.CharField(label='Количество*',widget=forms.TextInput(attrs={'class':'g-2',}))
    cost = forms.CharField(label='Ориентировочная цена',widget=forms.TextInput(attrs={'class':'g-2',}))
    analog = forms.CharField(label='Существующий аналог/Примечание',widget=forms.TextInput(attrs={'class':'g-5',}),required=False)



### --- Форма выбора пользователя из списка ---
class	UserChoiceForm(forms.Form):
    user = forms.ChoiceField(label='Пользователь *',required=False,choices=user_list)

    def	__init__(self,*args,**kwargs):
        super(UserChoiceForm,self).__init__(*args,**kwargs)
        self.fields['user'].choices = user_list


class	LoadFile(forms.Form):
    comment = forms.CharField(label='Описание документа (файла)*',widget=forms.Textarea)
    file_load = forms.FileField(label='Выбор документа (Файла)*',widget=forms.FileInput,required=False)


### --- Форма установки статусов ---
class	StatusForm(forms.Form):
    comment = forms.CharField(label='Комментарий',widget=forms.Textarea(attrs={'class':'g-5',}),required=False)
    status = forms.ChoiceField(label='Статус*',choices=GetStatusListAll())


### --- Форма отправки email руководителю ---
class	EmailForm(forms.Form):
    email = forms.ChoiceField(label='Выбор получателя сообщения',required=False,choices=GetEmailRukList())
    def	__init__(self,*args,**kwargs):
        super(EmailForm,self).__init__(*args,**kwargs)
        self.fields['email'].choices = GetEmailRukList()


### --- Форма перевода в группу ---
class	GroupForm(forms.Form):
    comment = forms.CharField(label='Комментарий',widget=forms.Textarea(attrs={'class':'g-5',}),required=False)
    group = forms.ChoiceField(label='Группа ТМЦ *',choices=GetTmcGroupList())


### --- Форма для шифра затрат ---
class	ShifrForm(forms.Form):
    shifr = forms.CharField(label='Шифр затрат',widget=forms.TextInput(attrs={'class':'g-5',}))


### --- Форма для редактирования заяви ТМЦ ---
class	EditTmcForm(forms.Form):
    tema = forms.CharField(label='Тема*',widget=forms.TextInput(attrs={'class':'g-5',}))
    text = forms.CharField(label='Текст заявки*',widget=forms.Textarea(attrs={'class':'g-5',}))
    project = forms.ChoiceField(label='Проект*', required=False)
    project_num = forms.CharField(label='Номер проекта', widget=forms.TextInput(attrs={'class': 'g-5', }), required=False)
    def __init__(self, *args, **kwargs):
        super(EditTmcForm, self).__init__(*args, **kwargs)
        self.fields['project'].choices = GetProjectsType()



### --- Форма для ввода номера заявки ---
class	NumberForm(forms.Form):
    n = forms.IntegerField(label='Номер заявки*',max_value=5000,min_value=1,widget=forms.TextInput(attrs={'class':'g-2',}))


### --- Поиск (для внутреннего заказа) ---
class	SearchOrderForm(forms.Form):
    search = forms.CharField(label='Строка поиска',required=False)


### --- Создание нового внутреннего заказа ---
class	OrderForm(forms.Form):
    tmc = forms.ChoiceField(label='Заявка ТМЦ *',required=False,choices=GetTmcOrder())
    project = forms.CharField(label='Проект *',widget=forms.TextInput(attrs={'class':'g-5',}))
    executor = forms.ChoiceField(label='Получатель *',required=False,choices=GetUserList())

    def	__init__(self,*args,**kwargs):
        super(OrderForm,self).__init__(*args,**kwargs)
        self.fields['executor'].choices = GetUserList()
        self.fields['tmc'].choices = GetTmcOrder()



### --- Формирование списка уведомлений по группам ТМЦ ---
class	GroupEmailForm(forms.Form):
    user_kod = forms.ChoiceField(label='Пользователь *',required=False,choices=user_list)
    group = forms.ChoiceField(label='Группа ТМЦ *',choices=tmcgroup)

    def	__init__(self,*args,**kwargs):
        super(GroupEmailForm,self).__init__(*args,**kwargs)
        self.fields['user_kod'].choices = user_list



### --- Отчет по содержанию заявок ---
class	ReportSpecForm(forms.Form):
    chief = forms.ChoiceField(label='Руководитель *',choices=user_list)
    start_date = forms.DateField(label='Дата (с)*',widget=SelectDateWidget(years=[2011,2012,2014,2014,2015,2016,2017,2018]),initial=datetime.date.today())
    end_date = forms.DateField(label='Дата (по)*',widget=SelectDateWidget(years=[2011,2012,2014,2014,2015,2016,2017,2018]),initial=datetime.date.today())

    def	__init__(self,*args,**kwargs):
        super(ReportSpecForm,self).__init__(*args,**kwargs)
        self.fields['chief'].choices = user_list
        self.fields['start_date'].initial = datetime.date.today()
        self.fields['end_date'].initial = datetime.date.today()

