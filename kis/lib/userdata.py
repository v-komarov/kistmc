#coding:utf-8



def	GetFio(request):
    return u"{} {} {}".format(request.session['key888']['lastname'],request.session['key888']['firstname'],request.session['key888']['surname'])


def	GetPhone(request):
    return u"{}".format(request.session['key888']['phone'])


def	GetEmail(request):
    return u"{}".format(request.session['key888']['email'])


def	GetUserKod(request):
    return u"{}".format(request.session['key888']['id'])


def GetFirstName(request):
    return u"{}".format(request.session['key888']['firstname'])


def GetSurName(request):
    return u"{}".format(request.session['key888']['surname'])


def GetLastName(request):
    return u"{}".format(request.session['key888']['lastname'])


def GetJob(request):
    return u"{}".format(request.session['key888']['job'])


def GetContractId(request):
    return u"{}".format(request.session['contract_id'])






def	CheckAccess(request):

    #user_id = GetUserKod(request)
    #contract_id = GetContractId(request)
    #return ChAccess(contract_id,user_id)
    return 'OK'





## -- Принадлежность к группе администрирования
def AccessAdmin(request):

    if 'tmcadmin' in request.session['key888']['groups']:
        return "OK"
    else:
        return "error"

