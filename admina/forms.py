#coding:utf-8

from django import forms



from kis.lib.tmc import GetUserList



class	UserForm(forms.Form):
    user = forms.ChoiceField(label='Выбор пользователя',required=False,choices=[])
    def	__init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        self.fields['user'].choices = GetUserList()

