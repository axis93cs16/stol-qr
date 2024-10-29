# coding=utf-8
#from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, FormView
#from contacts.forms import ContactsForm
#from contacts.models import Feedback
#from django.forms import ModelForm
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from stolovaya.models import stolovaya as modelstol
from stolovaya.models import stolovayainfodata, stolovayainfopit, stolovayapodacha, stolovayatalon, stolovayacategory, get_typesofeda,get_typesofinternat, stolovayapriemipishi, stolovayamedflag, stolovayainfopitafter, stolovayafactstol
from stolovaya.models import stolovayablkdata, stolovayadietflag
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect, HttpResponse, render
from django.db.models import Q
from django.http import JsonResponse
from operator import itemgetter, attrgetter
from django.contrib.sites.models import Site
#from copy import copy
import copy

mlgotaarrvseda = {'zavtrak':0,'obed':0,'poldnik':0,'ujin1':0,'ujin2':0, 'zavtrakg':0, 'obedk':0, 'obedkg1':0, 'obedkg2':0, 'obedkg3':0, 'internatp':0}
mlgotaarrvsedamed = {'zavtrak':0,'obed':0,'poldnik':0,'ujin1':0,'ujin2':0, 'zavtrakg':0, 'obedk':0, 'obedkg1':0, 'obedkg2':0, 'obedkg3':0, 'internatp':0}
mnachalkaclass = {'103A':0,'103B':0,'104A':0,'104B':0, '104V':0}#,'105A':0,'105B':0,'106A':0,'106B':0}
mlgotnikilistnach = {'lgota14':0, 'normal':0, 'dogovor1':0, 'dogovor2':0, 'dogovor3':0, 'internatp':0}
mlgotnikilistnachsum = {'internat14':0, 'lgota14':0}
mlgotnikiliststarsum = {'internat59':0, 'lgota59':0}
mlgotnikilistbol = {'lgota59':0}
medaqr = {'zavtrak':0, 'zavtrak2':0,'obed':0,'poldnik':0,'ujin1':0, 'ujin2':0}

@login_required
def AdminViewme(request): #EDIT-CLASSRUK
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['class-ed','stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")


    queryset = modelstol.objects.all().order_by('classname','fio')
#    datamodel = stolovayainfodata.objects.all()
    #1
    #lgotaarrlist = queryset.values('typeofeda')
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
#    unique_eda = sorted(set( val for dic in lgotaarrlist for val in dic.values()))
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))

    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1
    if idcl==0:
        return redirect('/login/?next=%s' % request.path)
#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    selit = selectitems2[0]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                if ((dicta.get('datepicker')[0] < dateminmax[1]) and (dicta.get('datepicker')[0] > dateminmax[0])):
                    datasek = dicta.get('datepicker')[0]
                else:
                    datasek = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")


        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            else:
                selit = selectitems2[0]
            datid = ''
            datchk = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]
            for objdi, objdc in arrdata:
                if datetime.now().timestamp()<(datetime.strptime(datasek,'%Y-%m-%d').replace(hour=9, minute=16)).timestamp():
#                    stolovayainfodata.objects.filter(datapit=datdate[0],uchid_id=objdi).delete()
                    stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                    alertmsg ='Данные ЗАПИСАНЫ Спасибо!'
                else:
                    alertmsg ='Вы пытаетесь ввести данные на сегодняшнюю дату после разрешенного времени(текущая дата 9.15)'

    datamodel1 = []
    sumuch = 0
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek, classname=str(selit))
    datamodel = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    datamodelbl = set(stolovayablkdata.objects.all())
    for stolm in queryset :

        stolm.medflag = False
        stolm = stolmedflagget(stolm, datasek, stolmed)

        if stolm.medflag == True:
            continue

        stolm.blockflag = False
        stolm = stolchkblock(stolm, datasek, datamodelbl)

        if str(selit) == stolm.classname:
            stolm.typeofeda = 'normal'
            stolm = stolcategoryget(stolm, datasek, stolcat)

            stolm.chkflag = False
            stolm = stolchkflagget(stolm, datasek, datamodel)
            if not (stolm.typeofeda == 'internat14' or stolm.typeofeda == 'internat59'):
                        datamodel1.append(stolm)
                        sumuch += 1

    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))

    context = {'queryset':queryset1,  'selectitems':selectitems2, 'selit':selit, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0, 'sumuch':sumuch}
    return render(request, 'stolovaya/stol-edit.html', context)








@login_required
def AdminViewmeint(request): #EDIT-INT
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['int-ed','stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")


    queryset = modelstol.objects.all().order_by('classname','fio')
#    datamodel = stolovayainfodata.objects.all()
    #1
#    lgotaarrlist = queryset.values('typeofeda')
#    list_of_unique_eda = {}#[]
#    unique_eda = sorted(set( val for dic in lgotaarrlist for val in dic.values()))
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))
    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    list_of_unique_class.update({idcl:'Все'})
    idcl=1
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1

#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    internatarr = modelstol.objects.filter(~Q(internat='normal')).values('internat')
    list_of_unique_int = {}#[]
    unique_int = sorted(set( val for dic in internatarr for val in dic.values()))
    list_of_unique_int.update({'internat':'Все'})
    idcl2=0
    for inter in unique_int:
        if str('stol-admin') in unique_groups:
            list_of_unique_int.update({idcl2:inter[:1]})
            idcl2+=1
        else:
            if str(inter) in unique_groups:
                list_of_unique_int.update({idcl2:inter[:1]})
                idcl2+=1

    selectintitems=list_of_unique_int
    if idcl2 == 0 :
        selectintitems[0]="None"
#    updatebase=0
    selitint = selectintitems[0]
    selit = selectitems2[0]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    stolcat = set(stolovayacategory.objects.all())

    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('selitint', 0) != 0:
                selitint = dicta.get('selitint')[0]
                del dicta['selitint']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")
#        if dicta.get('form9',0) !=0: #tempfunc
#            del dicta['form9']
#            del dicta['csrfmiddlewaretoken']
#            updatebase=1
#            from django.contrib.auth.models import Group, User
#            for itofcl in selectitems2.values():
#                if itofcl == 'Все':
#                    continue
#                user = User.objects.create_user(username=(itofcl+'-ruk'), password=("!"+itofcl+'!d'))
#                user = User.objects.get(username=(itofcl+'-ruk'))
#                new_group, created = Group.objects.get_or_create(name=itofcl)
#                my_group = Group.objects.get(name='class-ed')
#                my_group.user_set.add(user)
#            tmpfdatpit = datetime.strptime(datasek,'%Y-%m-%d').date()
#            tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
#            tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
#            for objcat in modelstol.objects.all().order_by('classname','typeofeda','fio'):
#                stolovayacategory(uchid_id=objcat.id,category=objcat.typeofeda,dateeda=datetime.now().date(),datetime1=datetime.now()).save()




        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            else:
                selit = selectitems2[0]
            if dicta.get('selitint', 0) != 0:
                selitint = dicta.get('selitint')[0]
                del dicta['selitint']
            datid = ''
            datchk = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]

            datamodelas = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
            stolpit = set(stolovayainfopit.objects.filter(datapit=datasek).order_by('datapittime'))

            for objdi, objdc in arrdata:
                if datetime.now().timestamp()<(datetime.strptime(datasek,'%Y-%m-%d').replace(hour=9, minute=16)).timestamp():
#                    stolovayainfodata.objects.filter(datapit=datdate[0],uchid_id=objdi).delete()
                    checkflag = False
                    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
                    for datm in filter(lambda x:x.uchid_id==int(objdi), datamodelas):#datamodel : #отмеченные дети
                        if datm.datazapis.timestamp() >= tmpfdatpittime.timestamp():
                            tmpfdatpittime = datm.datazapis
                            checkflag = datm.chkflag
                    typeofedasave = 'normal'
                    tmpfdatpit = datetime.strptime(datasek,'%Y-%m-%d').date()
                    tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
                    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
                    for objcat in filter(lambda x:x.uchid_id==int(objdi),stolcat):#stolovayacategory.objects.filter(uchid_id=stolm.id):
                        if objcat.dateeda >= tmpdatpit:
                            if tmpfdatpit >= objcat.dateeda :
                                if objcat.datetime1.timestamp() >= tmpfdatpittime.timestamp():
                                    tmpdatpit = objcat.dateeda
                                    tmpfdatpittime = objcat.datetime1
                                    typeofedasave = objcat.category
                    edaget = func_read_int(int(objdi), datasek, typeofedasave, modeldatapit=stolpit)
                    if datetime.now().timestamp()<(datetime.strptime(datasek,'%Y-%m-%d').replace(hour=7, minute=31)).timestamp():
                        if checkflag == False:
                            if objdc == 'False' or objdc == False:
                                #########################################КОСТЫЛЬ!!!!!########################
                                if (('zavtrak' in edaget) and ('obed' in edaget) and ('poldnik' in edaget) and ('ujin1' in edaget) and ('ujin2' in edaget)) :
                                #########################################КОСТЫЛЬ!!!!!########################
                                    stolovayainfopit(datapit=datasek, uchid_id=objdi, zavtrak=edaget['zavtrak'], obed=edaget['obed'], poldnik=edaget['poldnik'], ujin1=edaget['ujin1'], ujin2=edaget['ujin2'], datapittime=datetime.now()).save()
                                stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                            else:
                                stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                                #stolovayainfopit(datapit=datasek, uchid_id=objdi, zavtrak=edaget['zavtrak'], obed=edaget['obed'], poldnik=edaget['poldnik'], ujin1=edaget['ujin1'], ujin2=edaget['ujin2'], datapittime=datetime.now()).save()
                        else:
                            stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                        alertmsg ='Данные ЗАПИСАНЫ Спасибо!'
                        #alertmsg += str(edaget)
                    else:
                        if 'datapittime' in edaget:
                            if edaget['datapittime'] != None:
                                stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                                alertmsg ='Данные ЗАПИСАНЫ(!ЗАВТРАК уже не применен(записано из предыдущей отметки)!) Спасибо!'
                                #alertmsg += str(edaget)
                            else:
                                if checkflag == False:
                                    stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                                else:
                                    #########################################КОСТЫЛЬ!!!!!########################
                                    if (('zavtrak' in edaget) and ('obed' in edaget) and ('poldnik' in edaget) and ('ujin1' in edaget) and ('ujin2' in edaget)) :
                                    #########################################КОСТЫЛЬ!!!!!########################
                                        stolovayainfopit(datapit=datasek, uchid_id=objdi, zavtrak=False, obed=edaget['obed'], poldnik=edaget['poldnik'], ujin1=edaget['ujin1'], ujin2=edaget['ujin2'], datapittime=datetime.now()).save()
                                    stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                                alertmsg ='Данные ЗАПИСАНЫ(!ЗАВТРАК уже не применен(записано из предыдущей отметки)!) Спасибо!'
                                #alertmsg += str(edaget)
                else:
                    alertmsg='Вы пытаетесь ввести данные на сегодняшнюю дату после разрешенного времени(текущая дата 9.15)'

#    for qrit in queryset:
#        if qrit.classname == selit:
#            queryset1.append(qrit)
    datamodel1 = []
    sumuch = 0
    if selitint != 'Все':
        queryset = modelstol.objects.filter(internat=(selitint+'-level')).order_by('classname','fio')
#
    stolmed = set(stolovayamedflag.objects.all())
    stolpit = set(stolovayainfopit.objects.filter(datapit=datasek).order_by('datapittime'))
    stoldiet = set(stolovayadietflag.objects.all())
    datamodelas = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    queryset = set(queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek))
#    stolpit = set(stolovayainfopit.objects.filter(datapit=datasek).order_by('datapittime'))
    stolpodacha = stolovayapodacha.objects.filter(site=Site.objects.get_current())[:1].get()
    for stolm in queryset :
        stolm.typeofeda = 'normal'
        stolm = stolcategoryget(stolm, datasek, stolcat)
        stolm.medflag = False
        stolm = stolmedflagget(stolm, datasek, stolmed)
        stolm.dietflag = False
        stolm = stoldietflagget(stolm, datasek, stoldiet)
        
        if stolm.medflag == True:
            continue
        if stolm.internat == 'normal':
            continue
#        if ((not((stolm.typeofeda == 'internat14') or (stolm.typeofeda == 'internat59'))) or (stolm.medflag == True)):
#            continue

        stolm.eda = func_read_int(stolm.id, datasek, stolm.typeofeda, modeldatapit=stolpit)
        stolm = setpriemiformatnorm(stolm)
        tmpfdatpit = datetime.strptime(datasek,'%Y-%m-%d').date()
        tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        stolm.chkflag = False
        stolm = stolchkflagget(stolm, datasek, datamodelas)

        if str(selit) == 'Все':
            sumuch += 1
            datamodel1.append(stolm)
        else:
            if str(selit) == stolm.classname:
                sumuch += 1
                datamodel1.append(stolm)

    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda','classname','fio'))
    context = {'queryset':queryset,  'selectitems':selectitems2, 'selit':selit, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0, 'sumuch':sumuch, 'selectintitems':selectintitems, 'selitint':selitint, 'stolpodacha':stolpodacha}
    return render(request, 'stolovaya/stol-int-edit.html', context)










@login_required
def AdminViewstol(request): #VIEW
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-view','stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)

    stolovayamodel = modelstol.objects.all().order_by('classname','fio')#modelstol.objects.filter(classname=selit)
#    lgotaarr = Object()
#    setattr(lgotaarr, 'toe', '')
#    setattr(lgotaarr, 'val', '')
#    insa = 0
#    insb = 0
#2
    lgotaarrlist2 = stolovayamodel.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    unique_class1=unique_class.copy()
    unique_class2=unique_class.copy()
    idcl=0
    for class2 in unique_class1:
        list_of_unique_class.update({idcl:class2})#idcl:class2})
        idcl+=1
    selectitems = unique_class1
    selectitems2 = list_of_unique_class
    #2
    #3
    list_of_unique_class2 = {}
    msumuchall = {}
    for class3 in unique_class2:
        list_of_unique_class2.update({class3:0})
        msumuchall[class3] = {}
        msumuchall[class3].update({'normal': 0,'diet': 0})


#    sumuchall = list_of_unique_class2.copy()
    sumuchall = msumuchall.copy()
    #3

    #1
#    lgotaarrlist = stolovayamodel.values('typeofeda')
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
    list_of_unique_eda_class = {}#[]
    unique_eda =sorted(set( dic for dic,dic2 in lgotaarrlist ),key=len, reverse=True)
#    dici=0
#    unique_eda = []
#    unique_eda1 = []
#    for dic, dici2 in lgotaarrlist :
#        for val in dic[dici][0]:
#            unique_eda1.append(dic)
#        dici+=1
#    unique_eda = unique_eda1.copy()
    list_of_unique_eda_class={}
    list_of_unique_eda_med={}
    lgotaarrvs = {}
    lgotaarrvsmed = {}
    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
        lgotaarrvs[eda] = {}
        lgotaarrvs[eda].update({'normal': 0,'diet': 0})
        lgotaarrvsmed[eda] = {}
        lgotaarrvsmed[eda].update({'normal': 0,'diet': 0})


#    lgotaarrvs = copy.deepcopy(mlgotaarrvs)
#    lgotaarrvsmed = copy.deepcopy(mlgotaarrvs)
#    list_of_unique_eda.update({'medcenter':0})
    lgotaarrvseda = {}
    lgotaarrvsedamed = {}
    nachalkasum = {}
    for eda in mlgotaarrvseda:
        lgotaarrvseda[eda]={}
        lgotaarrvseda[eda].update({'normal': 0,'diet': 0})
        lgotaarrvsedamed[eda]={}
        lgotaarrvsedamed[eda].update({'normal': 0,'diet': 0})
        nachalkasum[eda]={}
        nachalkasum[eda].update({'normal': 0,'diet': 0})

#    lgotaarrvseda = copy.deepcopy(pmlgotaarrvseda)
#    lgotaarrvsedamed = copy.deepcopy(pmlgotaarrvseda)
    nachalkaclass = mnachalkaclass.copy()
    lgotnikilistnach = mlgotnikilistnach.copy()
    lgotnikilistnachsum = mlgotnikilistnachsum.copy()
    lgotnikiliststarsum = mlgotnikiliststarsum.copy()
    lgotnikilistbol = mlgotnikilistbol.copy()

    for class41 in unique_class:
        list_of_unique_eda_class[class41] = {}
        for eda in unique_eda:
            if ((str(class41) in nachalkaclass) and (str(eda) in lgotnikiliststarsum)):
                continue
            if (not(str(class41) in nachalkaclass) and (str(eda) in lgotnikilistnachsum)):
                continue
            list_of_unique_eda_class[class41].update({eda:0})

#        list_of_unique_eda_class[class41].update({'medcenter':0})

#            list_of_unique_eda_class.setdefault(eda,(}).update({class41:0})
    list_of_unique_eda_class_eda = {}
    for class42 in unique_class:
        list_of_unique_eda_class_eda[class42] = {}
        for eda in lgotaarrvseda:
            list_of_unique_eda_class_eda[class42].update({eda:0})


    lgotaarr = list_of_unique_eda.copy()
#    lgotaarrvs = list_of_unique_eda.copy()
#    for obj in list_of_unique_eda:
#        lgotaarrvs[obj] = {}
#        lgotaarrvs[obj].update({'normal': 0})
#        lgotaarrvs[obj].update({'diet': 0})
#    lgotaarrvs
#    nachalkasum = copy.deepcopy(lgotaarrvseda)
    lgotaarrvs2 = list_of_unique_eda_class.copy()

    #1

    
    #lgotaarrvs2

    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        del dicta['csrfmiddlewaretoken']
#        if datepicker
        if ((dicta.get('datepicker', 0) == 0) or (dicta.get('datepicker', 0) == '') or (dicta.get('datepicker', 0) == None) or (dicta.get('datepicker', 0) == '')):
            datasek = datetime.now().strftime("%Y-%m-%d")
        else:
            datasek = dicta.get('datepicker')[0]
        if dicta.get('selit', 0) != 0:
            if dicta.get('selit')[0] != '':
                selit = dicta.get('selit')[0]
            else:
                selit = selectitems2[0]
        else:
            selit = selectitems2[0]
    else:
        datasek = datetime.now().strftime("%Y-%m-%d")
        selit = selectitems2[0]
    datamodel = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    datamodel.lgota = ''
    sumuch = 0
    sumuchvs = 0
    datamodel1 = []
    datamodel2 = []
    dataret = []

    flagdata=0
#    tmpfdatpit = datetime.strptime(datasek,'%Y-%m-%d').date()
#    tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
#    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
#    obed1talons = 0
#    obed2talons = 0
#    for objcat in stolovayatalon.objects.filter(dateeda=datasek).order_by('-datetime1'):
#        if objcat.dateeda >= tmpdatpit:
#            tmpdatpit = objcat.dateeda
#            if tmpfdatpit == objcat.dateeda :
#                if objcat.datetime1.timestamp() >= tmpfdatpittime.timestamp():
#                    tmpfdatpittime = objcat.datetime1
#                    if objcat.catoftalon == 'obed1':
#                        obed1talons = objcat.numoftalons
#                    if objcat.catoftalon == 'obed2':
#                        obed2talons = objcat.numoftalons
#    lgotaarrvseda['obed1tal'] = obed1talons
#    lgotaarrvseda['obed2tal'] = obed2talons
    stolovayamodel = set(stolovayamodel.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek))
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    stoldiet = set(stolovayadietflag.objects.all())
    stolpodacha = stolovayapodacha.objects.filter(site=Site.objects.get_current())[:1].get()
    stolinfo = stolovayainfopit.objects.filter(datapit=datasek).order_by('datapittime')
    delta1day = timedelta(days=1)
    modeldatapitaf=set(stolovayainfopitafter.objects.filter(datapit=(datetime.strptime(datasek,'%Y-%m-%d').date()-delta1day).strftime("%Y-%m-%d")).order_by('-datapittime'))
    nachalka_zavtrak = 0
    nachalka_zavtrak_en = 0
    #internatetaj = {'2-level':0, '3-level':0, '4-level':0}
    datnumofweek = datetime.strptime(datasek,'%Y-%m-%d').weekday()

    for datm in stolovayamodel :
        datm.xvarx = 1
        datm.chkflag = False
        datm = stolchkflagget(datm, datasek, datamodel)
##new var
#        if ((datm.chkflag == 'True') or (datm.chkflag == True)):
#            continue
##new var

#        if not hasattr(datm, 'datazapis'):
#            if ((datm.classname == '1XKO') and (datnumofweek == 2)):


        datm.typeofeda = 'normal'
        datm = stolcategoryget(datm, datasek, stolcat)


        datm.medflag = False
        datm = stolmedflagget(datm, datasek, stolmed)

        datm.dietflag = False
        datm = stoldietflagget(datm, datasek, stoldiet)
        if datm.dietflag == False:
            dietflagtxt='normal'
        else:
            dietflagtxt='diet'
        datm.eda = lgotaarrvseda.copy()

        datm.datapit = datetime.strptime(datasek, "%Y-%m-%d").date()
        datm.lgota = datm.typeofeda


        if not hasattr(datm, 'datazapis'):
            if not((datm.typeofeda == 'internat14') or (datm.typeofeda == 'internat59') or (datm.typeofeda == 'internatp')):
                if (datnumofweek == 6):
                    continue
        ##################KOSTIL################################
#            if ((datm.classname == '103A') and (datm.typeofeda != 'internat14') and (datnumofweek == 5)):
#                continue
        ##################KOSTIL################################

        ####################################СБОР данных по базам все лишние отсеены#########################################
        if str(selit) == 'all':
            datamodel1.append(datm)
            sumuch += 1
            lgotaarr[datm.lgota] += 1
        if str(selit) == datm.classname: #таблица фамилии
            datamodel1.append(datm)
            sumuch += 1
            lgotaarr[datm.lgota] += 1
        if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
            datamodel1.append(datm)
            sumuch += 1
            lgotaarr[datm.lgota] += 1
        if str(selit) == 'noneda': #таблица не питающиеся
            if ((datm.chkflag == 'True') or (datm.chkflag == True)):
                datamodel1.append(datm)
                sumuch += 1
                lgotaarr[datm.lgota] += 1
        if str(selit) == 'yepeda': #таблица питающиеся
            if ((datm.chkflag == 'False') or (datm.chkflag == False)):
                datamodel1.append(datm)
                sumuch += 1
                lgotaarr[datm.lgota] += 1


        if ((datm.chkflag == 'False') or (datm.chkflag == False)):
            datm.eda5 = func_read_int_fact(datm.id, datasek, datm.typeofeda, modeldatapit=modeldatapitaf)
            if not 'datazapis' in datm.eda5:
                datm.eda.update(func_read(datm.id, datasek, datm.typeofeda, medflag=datm.medflag, timestolmodel=stolpodacha, modeldatapit=stolinfo))
            #datm = setpriemiformatnorm(datm)
            datm.eda3 = func_read_int_fact(datm.id, (datetime.strptime(datasek,'%Y-%m-%d').date()-delta1day).strftime("%Y-%m-%d"), datm.typeofeda, modeldatapit=modeldatapitaf)
            if ((datm.classname in nachalkaclass) and (datm.typeofeda in lgotnikilistnach)) :
                nachalka_zavtrak += 1
                if 'zavtrak' in datm.eda:
                    if ((datm.eda['zavtrakg'] == True) or (datm.eda['zavtrakg'] == 'True')):
                        nachalka_zavtrak_en += 1
                if 'zavtrak' in datm.eda3:
                    if ((datm.eda3['zavtrakg'] == True) or (datm.eda3['zavtrakg'] == 'True')):
                        nachalka_zavtrak_en += 1

            if datm.xvarx > 1:
            #####KOSTIL
                if datm.medflag == True:
                    lgotaarrvsmed[datm.lgota][dietflagtxt] += datm.xvarx
                    for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд med
                        if itemeda == 'True':
                            lgotaarrvsedamed[keyeda][dietflagtxt] += datm.xvarx
                else:
                    lgotaarrvs[datm.lgota][dietflagtxt] += (datm.xvarx - 1)
                    for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд
                        if itemeda == 'True':
                            lgotaarrvseda[keyeda][dietflagtxt] += (datm.xvarx - 1)
                            list_of_unique_eda_class_eda[datm.classname][keyeda] += (datm.xvarx - 1)
                            if datm.classname in nachalkaclass:
                                nachalkasum[keyeda][dietflagtxt] += (datm.xvarx - 1)
    
                    lgotaarrvs2[datm.classname][datm.lgota] += (datm.xvarx - 1)
                        
                #sumuchall[datm.classname] += 2
            #####KOSTIL
            #####NORM
            
            datamodel2.append(datm)

            if datm.medflag == True:
                lgotaarrvsmed[datm.lgota][dietflagtxt] += 1
                for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд med
                    if itemeda == 'True':
                        lgotaarrvsedamed[keyeda][dietflagtxt] +=1
            else:
                sumuchvs += 1
                lgotaarrvs[datm.lgota][dietflagtxt] += 1
                for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд
                    if itemeda == 'True':
                        lgotaarrvseda[keyeda][dietflagtxt] +=1
                        list_of_unique_eda_class_eda[datm.classname][keyeda] += 1
                        if datm.classname in nachalkaclass:
                            nachalkasum[keyeda][dietflagtxt] += 1
    
                lgotaarrvs2[datm.classname][datm.lgota] += 1
            
            sumuchall[datm.classname][dietflagtxt] += 1

#            for itemclass in selectitems:
#                if str(itemclass) == str(datm.classname):
#                    lgotaarrvs2[itemclass][datm.lgota] += 1
#                    sumuchall[itemclass] += 1


#    for itemclass in selectitems:
#        for lgotka in unique_eda:
#            if ((str(itemclass) in nachalkaclass) and (str(lgotka) in lgotnikiliststarsum)):
#                lgotaarrvs2[itemclass].pop(lgotka)
#            if (not(str(itemclass) in nachalkaclass) and (str(lgotka) in lgotnikilistnachsum)):
#                lgotaarrvs2[itemclass].pop(lgotka)
#    lgotaarrvs2[]
    #datamodel3 = ListAsQuerySet(datamodel2)
        datm = setpriemiformatnorm(datm)
        if str(selit) == 'zavtrak':
            if 'zavtrak' in datm.eda:
                if ((datm.eda['zavtrak'] == True) or (datm.eda['zavtrak'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
            if 'zavtrakg' in datm.eda:
                if ((datm.eda['zavtrakg'] == True) or (datm.eda['zavtrakg'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
            if 'internatp' in datm.eda:
                if ((datm.eda['internatp'] == True) or (datm.eda['internatp'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1


        if str(selit) == 'obed':
            if 'obed' in datm.eda:
                if ((datm.eda['obed'] == True) or (datm.eda['obed'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
            if 'obedkg1' in datm.eda:
                if ((datm.eda['obedkg1'] == True) or (datm.eda['obedkg1'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
            if 'obedkg2' in datm.eda:
                if ((datm.eda['obedkg2'] == True) or (datm.eda['obedkg2'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
            if 'obedkg3' in datm.eda:
                if ((datm.eda['obedkg3'] == True) or (datm.eda['obedkg3'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
            if 'internatp' in datm.eda:
                if ((datm.eda['internatp'] == True) or (datm.eda['internatp'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1


        if str(selit) == 'poldnik':
            if 'poldnik' in datm.eda:
                if ((datm.eda['poldnik'] == True) or (datm.eda['poldnik'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
            if 'internatp' in datm.eda:
                if ((datm.eda['internatp'] == True) or (datm.eda['internatp'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1

        if str(selit) == 'ujin1':
            if 'ujin1' in datm.eda:
                if ((datm.eda['ujin1'] == True) or (datm.eda['ujin1'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
            if 'internatp' in datm.eda:
                if ((datm.eda['internatp'] == True) or (datm.eda['internatp'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1

        if str(selit) == 'ujin2':
            if 'ujin2' in datm.eda:
                if ((datm.eda['ujin2'] == True) or (datm.eda['ujin2'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
            if 'internatp' in datm.eda:
                if ((datm.eda['internatp'] == True) or (datm.eda['internatp'] == 'True')):
                    datamodel1.append(datm)
                    sumuch += 1
                    lgotaarr[datm.lgota] += 1
                    
    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))
    context = {'nextqqq':datamodel0, 'nextartext':sumuch, 'lgotaarr':lgotaarr, 'nextartext2':sumuchvs, 'lgotaarr2':lgotaarrvs, 'datasek':datasek, 'selectitems':selectitems, 'selit':selit ,'sumuchall':sumuchall, 'lgotaarrvs2':lgotaarrvs2 , 'selectitems2':selectitems, 'lgotaarrvseda':lgotaarrvseda, 'lgotaarrvsmed':lgotaarrvsmed, 'lgotaarrvsedamed':lgotaarrvsedamed, 'datamodel2':datamodel2, 'nachalka_zavtrak':nachalka_zavtrak, 'nachalka_zavtrak_en':nachalka_zavtrak_en, 'list_of_unique_eda_class_eda':list_of_unique_eda_class_eda, 'nachalkasum':nachalkasum}
    return render(request, 'stolovaya/stol-view.html', context)


@login_required
def stoladminqr(request): #VIEW-qr
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-view','stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)

    stolovayamodel = modelstol.objects.all().order_by('classname','fio')#modelstol.objects.filter(classname=selit)
#2
    lgotaarrlist2 = stolovayamodel.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    unique_class1=unique_class.copy()
    unique_class2=unique_class.copy()
    idcl=0
    for class2 in unique_class1:
        list_of_unique_class.update({idcl:class2})#idcl:class2})
        idcl+=1
    selectitems = unique_class1
    selectitems2 = list_of_unique_class
    #2
    #3
    list_of_unique_class2 = {}
    for class3 in unique_class2:
        list_of_unique_class2.update({class3:0})
    sumuchall = list_of_unique_class2.copy()
    #3

    #1
#    lgotaarrlist = stolovayamodel.values('typeofeda')
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
    list_of_unique_eda_class = {}#[]
    unique_eda =sorted(set( dic for dic,dic2 in lgotaarrlist ),key=len, reverse=True)
    list_of_unique_eda_class={}
    list_of_unique_eda_med={}
    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
#    list_of_unique_eda.update({'medcenter':0})
    lgotaarrvseda = mlgotaarrvseda.copy()
    lgotaarrvsedamed = mlgotaarrvsedamed.copy()
    nachalkaclass = mnachalkaclass.copy()
    lgotnikilistnach = mlgotnikilistnach.copy()
    lgotnikilistnachsum = mlgotnikilistnachsum.copy()
    lgotnikiliststarsum = mlgotnikiliststarsum.copy()
    lgotnikilistbol = mlgotnikilistbol.copy()


    for class41 in unique_class:
        list_of_unique_eda_class[class41] = {}
        for eda in unique_eda:
            if ((str(class41) in nachalkaclass) and (str(eda) in lgotnikiliststarsum)):
                continue
            if (not(str(class41) in nachalkaclass) and (str(eda) in lgotnikilistnachsum)):
                continue
            list_of_unique_eda_class[class41].update({eda:0})

    list_of_unique_eda_class_eda = {}
    for class42 in unique_class:
        list_of_unique_eda_class_eda[class42] = {}
        for eda in lgotaarrvseda:
            list_of_unique_eda_class_eda[class42].update({eda:0})

    lgotaarr = list_of_unique_eda.copy()
    lgotaarrvs = list_of_unique_eda.copy()
    lgotaarrvs2 = list_of_unique_eda_class.copy()
    lgotaarrvsmed =list_of_unique_eda.copy()
    #1

    
    #lgotaarrvs2

    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        del dicta['csrfmiddlewaretoken']
#        if datepicker
        if ((dicta.get('datepicker', 0) == 0) or (dicta.get('datepicker', 0) == '') or (dicta.get('datepicker', 0) == None) or (dicta.get('datepicker', 0) == '')):
            datasek = datetime.now().strftime("%Y-%m-%d")
        else:
            datasek = dicta.get('datepicker')[0]
        if dicta.get('selit', 0) != 0:
            if dicta.get('selit')[0] != '':
                selit = dicta.get('selit')[0]
            else:
                selit = selectitems2[0]
        else:
            selit = selectitems2[0]
    else:
        datasek = datetime.now().strftime("%Y-%m-%d")
        selit = selectitems2[0]
    datamodel = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    datamodel.lgota = ''
    sumuch = 0
    sumuchvs = 0
    datamodel1 = []
    datamodel2 = []
    dataret = []

    flagdata=0
    stolovayamodel = set(stolovayamodel.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek))
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    stoldiet = set(stolovayadietflag.objects.all())
    stolpodacha = stolovayapodacha.objects.filter(site=Site.objects.get_current())[:1].get()
    stolinfo = stolovayainfopit.objects.filter(datapit=datasek).order_by('datapittime')
    delta1day = timedelta(days=1)
    modeldatapitaf=set(stolovayainfopitafter.objects.filter(datapit=(datetime.strptime(datasek,'%Y-%m-%d').date()-delta1day).strftime("%Y-%m-%d")).order_by('-datapittime'))
    nachalka_zavtrak = 0
    nachalka_zavtrak_en = 0
    datnumofweek = datetime.strptime(datasek,'%Y-%m-%d').weekday()
    qrcodesbase = stolovayafactstol.objects.filter(dateeda=datasek)
    for datm in stolovayamodel :
        datm.xvarx = 1
        datm.chkflag = False
        datm = stolchkflagget(datm, datasek, datamodel)
        if ((datm.chkflag == 'True') or (datm.chkflag == True)):
            continue
#        if not hasattr(datm, 'datazapis'):
#            if ((datm.classname == '1XKO') and (datnumofweek == 2)):
#                continue

        datm.typeofeda = 'normal'
        datm = stolcategoryget(datm, datasek, stolcat)

        datm.medflag = False
        datm = stolmedflagget(datm, datasek, stolmed)

        datm.dietflag = False
        datm = stoldietflagget(datm, datasek, stoldiet)

        datm.eda = lgotaarrvseda.copy()
        datm.eda9 = medaqr.copy()
        datm.datapit = datetime.strptime(datasek, "%Y-%m-%d").date()
        datm.lgota = datm.typeofeda


        if not hasattr(datm, 'datazapis'):
            if not((datm.typeofeda == 'internat14') or (datm.typeofeda == 'internat59') or (datm.typeofeda == 'internatp')):
                if (datnumofweek == 6):
                    continue
        ##################KOSTIL################################
#            if ((datm.classname == '103A') and (datm.typeofeda != 'internat14') and (datnumofweek == 5)):
#                continue
        ##################KOSTIL################################
        ####################################СБОР данных по базам все лишние отсеены#########################################
        datm.eda5 = func_read_int_fact(datm.id, datasek, datm.typeofeda, modeldatapit=modeldatapitaf)
        if not 'datazapis' in datm.eda5:
            datm.eda.update(func_read(datm.id, datasek, datm.typeofeda, medflag=datm.medflag, timestolmodel=stolpodacha, modeldatapit=stolinfo))
        datm.eda9.update(func_read_qr(datm.id, datasek, qrcodesbase=qrcodesbase))
        datm = setpriemiformatnorm(datm)
#        datm.eda3 = func_read_int_fact(datm.id, (datetime.strptime(datasek,'%Y-%m-%d').date()-delta1day).strftime("%Y-%m-%d"), datm.typeofeda, modeldatapit=modeldatapitaf)
#        if ((datm.classname in nachalkaclass) and (datm.typeofeda in lgotnikilistnach)) :
#            nachalka_zavtrak += 1
#            if 'zavtrak' in datm.eda:
#                if ((datm.eda['zavtrakg'] == True) or (datm.eda['zavtrakg'] == 'True')):
#                    nachalka_zavtrak_en += 1
#            if 'zavtrak' in datm.eda3:
#                if ((datm.eda3['zavtrakg'] == True) or (datm.eda3['zavtrakg'] == 'True')):
#                    nachalka_zavtrak_en += 1

        if ((datm.chkflag == 'False') or (datm.chkflag == False)):
            if datm.xvarx > 1:
            #####KOSTIL
                if datm.medflag == True:
                    lgotaarrvsmed[datm.lgota] += datm.xvarx
                    for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд med
                        if itemeda == 'True':
                            lgotaarrvsedamed[keyeda] += datm.xvarx
                    continue
                lgotaarrvs[datm.lgota] += (datm.xvarx - 1)
                for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд
                    if itemeda == 'True':
                        lgotaarrvseda[keyeda] += (datm.xvarx - 1)
                        list_of_unique_eda_class_eda[datm.classname][keyeda] += (datm.xvarx - 1)

                lgotaarrvs2[datm.classname][datm.lgota] += (datm.xvarx - 1)
                #sumuchall[datm.classname] += 2
            #####KOSTIL
            #####NORM
            sumuchvs += 1
            datamodel2.append(datm)
            if str(selit) == 'all':
                sumuch += 1
                lgotaarr[datm.lgota] += 1
                datamodel1.append(datm)
            if str(selit) == datm.classname: #таблица фамилии
                sumuch += 1
                lgotaarr[datm.lgota] += 1
                datamodel1.append(datm)
            if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                sumuch += 1
                lgotaarr[datm.lgota] += 1
                datamodel1.append(datm)
            if datm.medflag == True:
                lgotaarrvsmed[datm.lgota] += 1
                for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд med
                    if itemeda == 'True':
                        lgotaarrvsedamed[keyeda] +=1
                continue

            lgotaarrvs[datm.lgota] += 1
            for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд
                if itemeda == 'True':
                    lgotaarrvseda[keyeda] +=1
                    list_of_unique_eda_class_eda[datm.classname][keyeda] += 1

            lgotaarrvs2[datm.classname][datm.lgota] += 1
            sumuchall[datm.classname] += 1


    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))
    context = {'nextqqq':datamodel0, 'nextartext':sumuch, 'lgotaarr':lgotaarr, 'nextartext2':sumuchvs, 'lgotaarr2':lgotaarrvs, 'datasek':datasek, 'selectitems':selectitems, 'selit':selit ,'sumuchall':sumuchall, 'lgotaarrvs2':lgotaarrvs2 , 'selectitems2':selectitems, 'lgotaarrvseda':lgotaarrvseda, 'lgotaarrvsmed':lgotaarrvsmed, 'lgotaarrvsedamed':lgotaarrvsedamed, 'datamodel2':datamodel2, 'nachalka_zavtrak':nachalka_zavtrak, 'nachalka_zavtrak_en':nachalka_zavtrak_en, 'list_of_unique_eda_class_eda':list_of_unique_eda_class_eda}
    return render(request, 'stolovaya/stol-view-qr.html', context)



@login_required
def stoladminqrreport1(request): #VIEW-qr-report1
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-view','stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)

    stolovayamodel = modelstol.objects.all().order_by('classname','fio')#modelstol.objects.filter(classname=selit)
#2
    lgotaarrlist2 = stolovayamodel.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    unique_class1=unique_class.copy()
    unique_class2=unique_class.copy()
    idcl=0
    for class2 in unique_class1:
        list_of_unique_class.update({idcl:class2})#idcl:class2})
        idcl+=1
    selectitems = unique_class1
    selectitems2 = list_of_unique_class
    #2
    #3
    list_of_unique_class2 = {}
    for class3 in unique_class2:
        list_of_unique_class2.update({class3:0})
    sumuchall = list_of_unique_class2.copy()
    #3

    #1
#    lgotaarrlist = stolovayamodel.values('typeofeda')
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
    list_of_unique_eda_class = {}#[]
    unique_eda =sorted(set( dic for dic,dic2 in lgotaarrlist ),key=len, reverse=True)
    list_of_unique_eda_class={}
    list_of_unique_eda_med={}
    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
#    list_of_unique_eda.update({'medcenter':0})
    lgotaarrvseda = mlgotaarrvseda.copy()
    lgotaarrvsedamed = mlgotaarrvsedamed.copy()
    nachalkaclass = mnachalkaclass.copy()
    lgotnikilistnach = mlgotnikilistnach.copy()
    lgotnikilistnachsum = mlgotnikilistnachsum.copy()
    lgotnikiliststarsum = mlgotnikiliststarsum.copy()
    lgotnikilistbol = mlgotnikilistbol.copy()


    for class41 in unique_class:
        list_of_unique_eda_class[class41] = {}
        for eda in unique_eda:
            if ((str(class41) in nachalkaclass) and (str(eda) in lgotnikiliststarsum)):
                continue
            if (not(str(class41) in nachalkaclass) and (str(eda) in lgotnikilistnachsum)):
                continue
            list_of_unique_eda_class[class41].update({eda:0})

    list_of_unique_eda_class_eda = {}
    for class42 in unique_class:
        list_of_unique_eda_class_eda[class42] = {}
        for eda in lgotaarrvseda:
            list_of_unique_eda_class_eda[class42].update({eda:0})

    lgotaarr = list_of_unique_eda.copy()
    lgotaarrvs = list_of_unique_eda.copy()
    lgotaarrvs2 = list_of_unique_eda_class.copy()
    lgotaarrvsmed =list_of_unique_eda.copy()
    #1

    
    #lgotaarrvs2
    seliteda="obed"
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        del dicta['csrfmiddlewaretoken']
#        if datepicker
        if ((dicta.get('datepicker', 0) == 0) or (dicta.get('datepicker', 0) == '') or (dicta.get('datepicker', 0) == None) or (dicta.get('datepicker', 0) == '')):
            datasek = datetime.now().strftime("%Y-%m-%d")
        else:
            datasek = dicta.get('datepicker')[0]
        if dicta.get('selit', 0) != 0:
            if dicta.get('selit')[0] != '':
                selit = dicta.get('selit')[0]
            else:
                selit = selectitems2[0]
        else:
            selit = selectitems2[0]
        if dicta.get('seliteda', 0) != 0:
            seliteda = dicta.get('seliteda')[0]
    else:
        datasek = datetime.now().strftime("%Y-%m-%d")
        selit = selectitems2[0]
    datamodel = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    datamodel.lgota = ''
    sumuch = 0
    sumuchvs = 0
    datamodel1 = []
    datamodel2 = []
    dataret = []

    flagdata=0
    stolovayamodel = set(stolovayamodel.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek))
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    stoldiet = set(stolovayadietflag.objects.all())
    stolpodacha = stolovayapodacha.objects.filter(site=Site.objects.get_current())[:1].get()
    stolinfo = stolovayainfopit.objects.filter(datapit=datasek).order_by('datapittime')
    delta1day = timedelta(days=1)
    modeldatapitaf=set(stolovayainfopitafter.objects.filter(datapit=(datetime.strptime(datasek,'%Y-%m-%d').date()-delta1day).strftime("%Y-%m-%d")).order_by('-datapittime'))
    nachalka_zavtrak = 0
    nachalka_zavtrak_en = 0
    datnumofweek = datetime.strptime(datasek,'%Y-%m-%d').weekday()
    qrcodesbase = stolovayafactstol.objects.filter(dateeda=datasek)
    for datm in stolovayamodel :
        datm.chkflag = False
        datm.xvarx = 1
        datm = stolchkflagget(datm, datasek, datamodel)
        if ((datm.chkflag == 'True') or (datm.chkflag == True)):
            continue
#        if not hasattr(datm, 'datazapis'):
#            if ((datm.classname == '1XKO') and (datnumofweek == 2)):
#                continue

        datm.typeofeda = 'normal'
        datm = stolcategoryget(datm, datasek, stolcat)

        datm.medflag = False
        datm = stolmedflagget(datm, datasek, stolmed)

        datm.dietflag = False
        datm = stoldietflagget(datm, datasek, stoldiet)

        datm.eda = lgotaarrvseda.copy()
        datm.eda9 = medaqr.copy()
        datm.datapit = datetime.strptime(datasek, "%Y-%m-%d").date()
        datm.lgota = datm.typeofeda


        if not hasattr(datm, 'datazapis'):
            if not((datm.typeofeda == 'internat14') or (datm.typeofeda == 'internat59') or (datm.typeofeda == 'internatp')):
                if (datnumofweek == 6):
                    continue
        ##################KOSTIL################################
#            if ((datm.classname == '103A') and (datm.typeofeda != 'internat14') and (datnumofweek == 5)):
#                continue
        ##################KOSTIL################################
        ####################################СБОР данных по базам все лишние отсеены#########################################
        datm.eda5 = func_read_int_fact(datm.id, datasek, datm.typeofeda, modeldatapit=modeldatapitaf)
        if not 'datazapis' in datm.eda5:
            datm.eda.update(func_read(datm.id, datasek, datm.typeofeda, medflag=datm.medflag, timestolmodel=stolpodacha, modeldatapit=stolinfo))
        datm.eda9.update(func_read_qr(datm.id, datasek, qrcodesbase=qrcodesbase))
        datm = setpriemiformatnorm(datm)
#        datm.eda3 = func_read_int_fact(datm.id, (datetime.strptime(datasek,'%Y-%m-%d').date()-delta1day).strftime("%Y-%m-%d"), datm.typeofeda, modeldatapit=modeldatapitaf)
#        if ((datm.classname in nachalkaclass) and (datm.typeofeda in lgotnikilistnach)) :
#            nachalka_zavtrak += 1
#            if 'zavtrak' in datm.eda:
#                if ((datm.eda['zavtrakg'] == True) or (datm.eda['zavtrakg'] == 'True')):
#                    nachalka_zavtrak_en += 1
#            if 'zavtrak' in datm.eda3:
#                if ((datm.eda3['zavtrakg'] == True) or (datm.eda3['zavtrakg'] == 'True')):
#                    nachalka_zavtrak_en += 1

        if ((datm.chkflag == 'False') or (datm.chkflag == False)):
            if datm.xvarx > 1:
            #####KOSTIL
                if datm.medflag == True:
                    lgotaarrvsmed[datm.lgota] += datm.xvarx
                    for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд med
                        if itemeda == 'True':
                            lgotaarrvsedamed[keyeda] += datm.xvarx
                    continue
                lgotaarrvs[datm.lgota] += (datm.xvarx - 1)
                for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд
                    if itemeda == 'True':
                        lgotaarrvseda[keyeda] += (datm.xvarx - 1)
                        list_of_unique_eda_class_eda[datm.classname][keyeda] += (datm.xvarx - 1)

                lgotaarrvs2[datm.classname][datm.lgota] += (datm.xvarx - 1)
                #sumuchall[datm.classname] += 2
            #####KOSTIL
            #####NORM
            sumuchvs += 1
            datamodel2.append(datm)
            
            
#            if str(selit) == 'all':
#            if str(seliteda) == 'obed':
            if not (datm.classname in nachalkaclass):
                if datm.medflag == "True" or datm.medflag == True:
                    continue
                if str(seliteda) == 'zavtrak':
                    if 'zavtrak' in datm.eda:
                        if ((datm.eda['zavtrak'] == True) or (datm.eda['zavtrak'] == "True") or (datm.eda['zavtrak'] == "true") or (datm.eda['zavtrak'] == 1)):
                            if 'zavtrak' in datm.eda9:
                                if ((datm.eda9['zavtrak'] == False) or (datm.eda9['zavtrak'] == "False") or (datm.eda9['zavtrak'] == "false") or (datm.eda9['zavtrak'] == 0) or (datm.eda9['zavtrak']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                    if 'zavtrakg' in datm.eda:
                        if ((datm.eda['zavtrakg'] == True) or (datm.eda['zavtrakg'] == "True") or (datm.eda['zavtrakg'] == "true") or (datm.eda['zavtrakg'] == 1)):
                            if 'zavtrak' in datm.eda9:
                                if ((datm.eda9['zavtrak'] == False) or (datm.eda9['zavtrak'] == "False") or (datm.eda9['zavtrak'] == "false") or (datm.eda9['zavtrak'] == 0) or (datm.eda9['zavtrak']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                if str(seliteda) == 'obed':
                    if 'obed' in datm.eda:
                        if ((datm.eda['obed'] == True) or (datm.eda['obed'] == "True") or (datm.eda['obed'] == "true") or (datm.eda['obed'] == 1)):
                            if 'obed' in datm.eda9:
                                if ((datm.eda9['obed'] == False) or (datm.eda9['obed'] == "False") or (datm.eda9['obed'] == "false") or (datm.eda9['obed'] == 0) or (datm.eda9['obed']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                    if 'obedk' in datm.eda:
                        if ((datm.eda['obedk'] == True) or (datm.eda['obedk'] == "True") or (datm.eda['obedk'] == "true") or (datm.eda['obedk'] == 1)):
                            if 'obed' in datm.eda9:
                                if ((datm.eda9['obed'] == False) or (datm.eda9['obed'] == "False") or (datm.eda9['obed'] == "false") or (datm.eda9['obed'] == 0) or (datm.eda9['obed']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1

                    if 'obedkg1' in datm.eda:
                        if ((datm.eda['obedkg1'] == True) or (datm.eda['obedkg1'] == "True") or (datm.eda['obedkg1'] == "true") or (datm.eda['obedkg1'] == 1)):
                            if 'obed' in datm.eda9:
                                if ((datm.eda9['obed'] == False) or (datm.eda9['obed'] == "False") or (datm.eda9['obed'] == "false") or (datm.eda9['obed'] == 0) or (datm.eda9['obed']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1


                    if 'obedkg2' in datm.eda:
                        if ((datm.eda['obedkg2'] == True) or (datm.eda['obedkg2'] == "True") or (datm.eda['obedkg2'] == "true") or (datm.eda['obedkg2'] == 1)):
                            if 'obed' in datm.eda9:
                                if ((datm.eda9['obed'] == False) or (datm.eda9['obed'] == "False") or (datm.eda9['obed'] == "false") or (datm.eda9['obed'] == 0) or (datm.eda9['obed']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1


                    if 'obedkg3' in datm.eda:
                        if ((datm.eda['obedkg3'] == True) or (datm.eda['obedkg3'] == "True") or (datm.eda['obedkg3'] == "true") or (datm.eda['obedkg3'] == 1)):
                            if 'obed' in datm.eda9:
                                if ((datm.eda9['obed'] == False) or (datm.eda9['obed'] == "False") or (datm.eda9['obed'] == "false") or (datm.eda9['obed'] == 0) or (datm.eda9['obed']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                    if 'internatp' in datm.eda:
                        if ((datm.eda['internatp'] == True) or (datm.eda['internatp'] == "True") or (datm.eda['internatp'] == "true") or (datm.eda['internatp'] == 1)):
                            if 'obed' in datm.eda9:
                                if ((datm.eda9['obed'] == False) or (datm.eda9['obed'] == "False") or (datm.eda9['obed'] == "false") or (datm.eda9['obed'] == 0) or (datm.eda9['obed']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1





                if str(seliteda) == 'poldnik':
                    if 'poldnik' in datm.eda:
                        if ((datm.eda['poldnik'] == True) or (datm.eda['poldnik'] == "True") or (datm.eda['poldnik'] == "true") or (datm.eda['poldnik'] == 1)):
                            if 'poldnik' in datm.eda9:
                                if ((datm.eda9['poldnik'] == False) or (datm.eda9['poldnik'] == "False") or (datm.eda9['poldnik'] == "false") or (datm.eda9['poldnik'] == 0) or (datm.eda9['poldnik']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1

                if str(seliteda) == 'ujin1':
                    if 'ujin1' in datm.eda:
                        if ((datm.eda['ujin1'] == True) or (datm.eda['ujin1'] == "True") or (datm.eda['ujin1'] == "true") or (datm.eda['ujin1'] == 1)):
                            if 'ujin1' in datm.eda9:
                                if ((datm.eda9['ujin1'] == False) or (datm.eda9['ujin1'] == "False") or (datm.eda9['ujin1'] == "false") or (datm.eda9['ujin1'] == 0) or (datm.eda9['ujin1']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1

                if str(seliteda) == 'ujin2':
                    if 'ujin2' in datm.eda:
                        if ((datm.eda['ujin2'] == True) or (datm.eda['ujin2'] == "True") or (datm.eda['ujin2'] == "true") or (datm.eda['ujin2'] == 1)):
                            if 'ujin2' in datm.eda9:
                                if ((datm.eda9['ujin2'] == False) or (datm.eda9['ujin2'] == "False") or (datm.eda9['ujin2'] == "false") or (datm.eda9['ujin2'] == 0) or (datm.eda9['ujin2']=='')):
                                    if str(selit) == 'all':
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == datm.classname: #таблица фамилии
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1
                                    if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
                                        datamodel1.append(datm)
                                        sumuch += 1
                                        lgotaarr[datm.lgota] += 1

#                else:
#                    datamodel1.append(datm)
#            if str(selit) == datm.classname: #таблица фамилии
#                sumuch += 1
#                lgotaarr[datm.lgota] += 1
#                datamodel1.append(datm)
#            if str(selit) == 'med' and datm.medflag == True: #таблица фамилии МЕДЦЕНТРА
#                sumuch += 1
#                lgotaarr[datm.lgota] += 1
#                datamodel1.append(datm)
            if datm.medflag == True:
                lgotaarrvsmed[datm.lgota] += 1
                for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд med
                    if itemeda == 'True':
                        lgotaarrvsedamed[keyeda] +=1
                continue

            lgotaarrvs[datm.lgota] += 1
            for keyeda,itemeda in datm.eda.items(): #по приемам пищи обед ужин итд
                if itemeda == 'True':
                    lgotaarrvseda[keyeda] +=1
                    list_of_unique_eda_class_eda[datm.classname][keyeda] += 1

            lgotaarrvs2[datm.classname][datm.lgota] += 1
            sumuchall[datm.classname] += 1


    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))
    context = {'nextqqq':datamodel0, 'nextartext':sumuch, 'lgotaarr':lgotaarr, 'nextartext2':sumuchvs, 'lgotaarr2':lgotaarrvs, 'datasek':datasek, 'selectitems':selectitems, 'selit':selit ,'sumuchall':sumuchall, 'lgotaarrvs2':lgotaarrvs2 , 'selectitems2':selectitems, 'lgotaarrvseda':lgotaarrvseda, 'lgotaarrvsmed':lgotaarrvsmed, 'lgotaarrvsedamed':lgotaarrvsedamed, 'datamodel2':datamodel2, 'nachalka_zavtrak':nachalka_zavtrak, 'nachalka_zavtrak_en':nachalka_zavtrak_en, 'list_of_unique_eda_class_eda':list_of_unique_eda_class_eda, 'seliteda':seliteda}
    return render(request, 'stolovaya/stol-view-qr-r.html', context)



@login_required
def form_test(request, *args, **kwargs): #Обработчк от модальных окон СОХРАНИТЬ!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-view','stol-admin','stol-med','int-ed','class-ed', 'med-ed']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['uchid'] = dicta.get('uchid')[0]
            data['datpit'] = dicta.get('datpit')[0]
            data['zavtrak'] = dicta.get('zavtrak')[0].lower().capitalize() if dicta.get('zavtrak','Fail') != 'Fail' else None
            data['obed'] = dicta.get('obed')[0].lower().capitalize() if dicta.get('obed','Fail') != 'Fail' else None
            data['poldnik'] = dicta.get('poldnik')[0].lower().capitalize() if dicta.get('poldnik','Fail') != 'Fail' else None
            data['ujin1'] = dicta.get('ujin1')[0].lower().capitalize() if dicta.get('ujin1','Fail') != 'Fail' else None
            data['ujin2'] = dicta.get('ujin2')[0].lower().capitalize() if dicta.get('ujin2','Fail') != 'Fail' else None
            data['obedk'] = dicta.get('obedk')[0].lower().capitalize() if dicta.get('obedk','Fail') != 'Fail' else None
            data['obedkg1'] = dicta.get('obedkg1')[0].lower().capitalize() if dicta.get('obedkg1','Fail') != 'Fail' else None
            data['obedkg2'] = dicta.get('obedkg2')[0].lower().capitalize() if dicta.get('obedkg2','Fail') != 'Fail' else None
            data['obedkg3'] = dicta.get('obedkg3')[0].lower().capitalize() if dicta.get('obedkg3','Fail') != 'Fail' else None
            data['internatp'] = dicta.get('internatp')[0].lower().capitalize() if dicta.get('internatp','Fail') != 'Fail' else None
            data['zavtrakg'] = dicta.get('zavtrakg')[0].lower().capitalize() if dicta.get('zavtrakg','Fail') != 'Fail' else None
            typeofeda = 'normal'
            tmpfdatpit = datetime.strptime(data['datpit'],'%Y-%m-%d').date()
            tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
            tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
            for objcat in stolovayacategory.objects.filter(uchid_id=data['uchid']):
                if objcat.dateeda >= tmpdatpit:
                    if tmpfdatpit >= objcat.dateeda :
                        if objcat.datetime1.timestamp() >= tmpfdatpittime.timestamp():
                            tmpdatpit = objcat.dateeda
                            tmpfdatpittime = objcat.datetime1
                            typeofeda = objcat.category
            dat={'zavtrak':None, 'obed':None, 'poldnik':None, 'ujin1':None, 'ujin2':None, 'zavtrakg':None, 'obedk':None, 'obedkg1':None, 'obedkg2':None, 'obedkg3':None, 'internatp':None}
            modeldatapit=set(stolovayainfopit.objects.filter(datapit=str(data['datpit'])).order_by('-datapittime'))
            dat.update(func_read_int(fuchid=data['uchid'], fdatpit=data['datpit'], flgota=typeofeda,modeldatapit=modeldatapit))
            data['disa'] = str(dat)
            if dicta.get('medflag', 0) != 0:
                timeforcez = None
                timeforceo = None
                timeforcep = None
                timeforceu1 = None
                timeforceu2 = None
                timeforceok = None
                timeforceokg1 = None
                timeforceokg2 = None
                timeforceokg3 = None
                timeforceozg = None
                timeforceip = None
                timestolmodel = stolovayapodacha.objects.filter(site=Site.objects.get_current())[:1].get()
                timestolmodel2 = stolovayapriemipishi.objects.filter(site=Site.objects.get_current())[:1].get()
                data['alertmsg'] = ''
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.zavtrak.hour), minute=int(timestolmodel.zavtrak.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforcez = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.zavtrak.hour), minute=int(timestolmodel2.zavtrak.minute)).timestamp()):#принудит завтрак кончен
                        data['alertmsg'] += 'время для заказа завтрака уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время завтрака уже закончилось(не применено)<br>'
                        data['zavtrak'] = dat['zavtrak']
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obed.hour), minute=int(timestolmodel.obed.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforceo = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.obed.hour), minute=int(timestolmodel2.obed.minute)).timestamp()):#принудит обед кончен
                        data['alertmsg'] += 'время для заказа обеда уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время обеда уже закончилось(не применено)<br>'
                        data['obed'] = dat['obed']
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.poldnik.hour), minute=int(timestolmodel.poldnik.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforcep = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.poldnik.hour), minute=int(timestolmodel2.poldnik.minute)).timestamp()):#принудит полдник кончен
                        data['alertmsg'] += 'время для заказа полдника уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время полдника уже закончилось(не применено)<br>'
                        data['poldnik'] = dat['poldnik']
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.ujin1.hour), minute=int(timestolmodel.ujin1.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforceu1 = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.ujin1.hour), minute=int(timestolmodel2.ujin1.minute)).timestamp()):#принудит ужин1 кончен
                        data['alertmsg'] += 'время для заказа ужина1 уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время ужина1 уже закончилось(не применено)<br>'
                        data['ujin1'] = dat['ujin1']
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.ujin2.hour), minute=int(timestolmodel.ujin2.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforceu2 = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.ujin2.hour), minute=int(timestolmodel2.ujin2.minute)).timestamp()):#принудит ужин2 кончен
                        data['alertmsg'] += 'время для заказа ужина2 уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время ужина2 уже закончилось(не применено)<br>'
                        data['ujin2'] = dat['ujin2']
                        
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obedk.hour), minute=int(timestolmodel.obedk.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforceok = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.obedk.hour), minute=int(timestolmodel2.obedk.minute)).timestamp()):#принудит обедк кончен
                        data['alertmsg'] += 'время для заказа комплексного уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время комплексного уже закончилось(не применено)<br>'
                        data['obedk'] = dat['obedk']
                        
                        
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obedkg1.hour), minute=int(timestolmodel.obedkg1.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforceokg1 = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.obedkg1.hour), minute=int(timestolmodel2.obedkg1.minute)).timestamp()):#принудит обедк кончен
                        data['alertmsg'] += 'время для заказа договора-тип1 уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время договора-тип1 уже закончилось(не применено)<br>'
                        data['obedkg1'] = dat['obedkg1']
                        
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obedkg2.hour), minute=int(timestolmodel.obedkg2.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforceokg2 = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.obedkg2.hour), minute=int(timestolmodel2.obedkg2.minute)).timestamp()):#принудит обедк кончен
                        data['alertmsg'] += 'время для заказа договора-тип2 уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время договора-тип2 уже закончилось(не применено)<br>'
                        data['obedkg2'] = dat['obedkg2']
                        
                        
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obedkg3.hour), minute=int(timestolmodel.obedkg3.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforceokg3 = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.obedkg3.hour), minute=int(timestolmodel2.obedkg3.minute)).timestamp()):#принудит обедк кончен
                        data['alertmsg'] += 'время для заказа договора-тип3 уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время договора-тип3 уже закончилось(не применено)<br>'
                        data['obedkg3'] = dat['obedkg3']
                        
                        
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.zavtrak.hour), minute=int(timestolmodel.zavtrak.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforceip = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.zavtrak.hour), minute=int(timestolmodel2.zavtrak.minute)).timestamp()):#принудит zavtrak кончен
                        data['alertmsg'] += 'время для заказа Интернат-Платники уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время Интернат-Платники уже закончилось(не применено)<br>'
                        data['internatp'] = dat['internatp']
                        
                if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.zavtrakg.hour), minute=int(timestolmodel.zavtrakg.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    timeforceozg = datetime.now()
                else:
                    if datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel2.zavtrakg.hour), minute=int(timestolmodel2.zavtrakg.minute)).timestamp()):#принудит zavtrakg кончен
                        data['alertmsg'] += 'время для заказа завтрак(льгот) уже закончилось(сообщите что вы поменяли)<br>'
                    else:
                        data['alertmsg'] += 'время завтрак(льгот) уже закончилось(не применено)<br>'
                        data['zavtrakg'] = dat['zavtrakg']
                        
                stolovayainfopit(datapit=data['datpit'], uchid_id=data['uchid'], zavtrak=data['zavtrak'], obed=data['obed'], poldnik=data['poldnik'], ujin1=data['ujin1'], ujin2=data['ujin2'], obedk=data['obedk'], obedkg1=data['obedkg1'], obedkg2=data['obedkg2'], obedkg3=data['obedkg3'], internatp=data['internatp'], zavtrakg=data['zavtrakg'], datapittime=datetime.now(), forceflago=timeforceo,forceflagp=timeforcep,forceflagz=timeforcez,forceflagu1=timeforceu1,forceflagu2=timeforceu2,forceflagok=timeforceok,forceflagokg1=timeforceokg1,forceflagokg2=timeforceokg2,forceflagokg3=timeforceokg3,forceflagozg=timeforceozg, forceflagip=timeforceip, forceflagmed=datetime.now() ).save()
            else:
                timestolmodel = stolovayapodacha.objects.filter(site=Site.objects.get_current())[:1].get()
                data['alertmsg'] = ''
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.zavtrak.hour), minute=int(timestolmodel.zavtrak.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа завтрака уже закончилось<br>'
                    data['zavtrak']=dat['zavtrak']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obed.hour), minute=int(timestolmodel.obed.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа обеда уже закончилось<br>'
                    data['obed']=dat['obed']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.poldnik.hour), minute=int(timestolmodel.poldnik.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа полдника уже закончилось<br>'
                    data['poldnik']=dat['poldnik']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.ujin1.hour), minute=int(timestolmodel.ujin1.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа ужина1 уже закончилось<br>'
                    data['ujin1']=dat['ujin1']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.ujin2.hour), minute=int(timestolmodel.ujin2.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа ужина2 уже закончилось<br>'
                    data['ujin2']=dat['ujin2']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obedk.hour), minute=int(timestolmodel.obedk.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа комплексного уже закончилось<br>'
                    data['obedk']=dat['obedk']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obedkg1.hour), minute=int(timestolmodel.obedkg1.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа договор-тип1 уже закончилось<br>'
                    data['obedkg1']=dat['obedkg1']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obedkg2.hour), minute=int(timestolmodel.obedkg2.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа договор-тип2 уже закончилось<br>'
                    data['obedkg2']=dat['obedkg2']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.obedkg3.hour), minute=int(timestolmodel.obedkg3.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа договор-тип3 уже закончилось<br>'
                    data['obedkg3']=dat['obedkg3']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.zavtrak.hour), minute=int(timestolmodel.zavtrak.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа Интернат-Платники уже закончилось<br>'
                    data['internatp']=dat['internatp']
                if not datetime.now().timestamp()<(datetime.strptime(data['datpit'],'%Y-%m-%d').replace(hour=int(timestolmodel.zavtrakg.hour), minute=int(timestolmodel.zavtrakg.minute)).timestamp()):#принудит ставим флаг и надо alertmsg
                    data['alertmsg'] += 'время для заказа завтрак-г уже закончилось<br>'
                    data['zavtrakg']=dat['zavtrakg']
                stolovayainfopit(datapit=data['datpit'], uchid_id=data['uchid'], zavtrak=data['zavtrak'], obed=data['obed'], poldnik=data['poldnik'], ujin1=data['ujin1'], ujin2=data['ujin2'], obedk=data['obedk'], obedkg1=data['obedkg1'], obedkg2=data['obedkg2'], obedkg3=data['obedkg3'], zavtrakg=data['zavtrakg'], internatp=data['internatp'], datapittime=datetime.now()).save()
            data['success'] = 'ok'
    context = {'data':data}
    return JsonResponse(data)

@login_required
def form_test2(request, *args, **kwargs): #Обработчк от модальных окон ПРОЧИТАТЬ!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-view','stol-admin','int-ed', 'class-ed']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
#    data['uchid'] = '1'
#    data['datpit'] = '2022-12-06'
#    modeldatapit = stolovayainfopit.objects.filter(datapit=data['datpit'], uchid_id=data['uchid'])
#    data['count'] = modeldatapit.count()
#    data['z'] = str(modeldatapit.values_list())
#    data['k'] = str(modeldatapit.values())
#    data['zav'] = next(x.zavtrak for x in modeldatapit)
#    modeldatapit = stolovayainfopit.objects.filter(datapit=data['datpit'], uchid_id=data['uchid'])
#    if modeldatapit.count() > 0 :
#        for xobj in modeldatapit:
#            data['zavtrak'] = str(xobj.zavtrak).lower().capitalize()
#            data['obed'] = str(xobj.obed).lower().capitalize()
#            data['poldnik'] = str(xobj.poldnik).lower().capitalize()
#            data['ujin1'] = str(xobj.ujin1).lower().capitalize()
#            data['ujin2'] = str(xobj.ujin2).lower().capitalize()
#            break
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['uchid'] = dicta.get('uchid')[0]
            data['datpit'] = dicta.get('datpit')[0]
            #modelstol1 = modelstol.objects.filter(Q(typeofeda='internat14') | Q(typeofeda='internat59')).order_by('classname','typeofeda','fio')
            modeldatapit = stolovayainfopit.objects.filter(datapit=str(data['datpit']), uchid_id=data['uchid']).order_by(datapittime)
#            for objm1 in modelstol1:
#                for objpit1 in modeldatapit:
            if modeldatapit.count() > 0 :
                for xobj in modeldatapit:
                    data['zavtrak'] = str(xobj.zavtrak).lower().capitalize()
                    data['obed'] = str(xobj.obed).lower().capitalize()
                    data['poldnik'] = str(xobj.poldnik).lower().capitalize()
                    data['ujin1'] = str(xobj.ujin1).lower().capitalize()
                    data['ujin2'] = str(xobj.ujin2).lower().capitalize()
                    break
            else:
                data['zavtrak'] = "true".lower().capitalize()
                data['obed'] = "true".lower().capitalize()
                data['poldnik'] = "true".lower().capitalize()
                data['ujin1'] = "true".lower().capitalize()
                data['ujin2'] = "true".lower().capitalize()
    context = {'data':data}
    return JsonResponse(data)

def func_read_qr(fuchid, fdatpit, qrcodesbase):
    data = {}
    data['uchid'] = fuchid
    data['datpit'] = fdatpit
    data['zavtrak'] = ''
    data['zavtrak2'] = ''
    data['obed'] = ''
    data['poldnik'] = ''
    data['ujin1'] = ''
    data['ujin2'] = ''
    qrcodesbase = list(filter(lambda x:((str(x.dateeda)==fdatpit) and (x.uchid_id==int(fuchid))), qrcodesbase))
    tmpfdatpit = datetime.strptime(fdatpit,'%Y-%m-%d').date()
    tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
    if len(qrcodesbase) >0 :
        for xobj in qrcodesbase:
            if xobj.dateeda >= tmpdatpit:
                if tmpfdatpit == xobj.dateeda:
                    if xobj.datetime.timestamp() >= tmpfdatpittime.timestamp():
                        tmpdatpit = xobj.dateeda
                        tmpfdatpittime = xobj.datetime
                        if (xobj.typeofedapit=='zavtrak'): data['zavtrak'] = True
                        if (xobj.typeofedapit=='zavtrak2'): data['zavtrak2'] = True
                        if (xobj.typeofedapit=='obed'): data['obed'] = True
                        if (xobj.typeofedapit=='poldnik'): data['poldnik'] = True
                        if (xobj.typeofedapit=='ujin1'): data['ujin1'] = True
                        if (xobj.typeofedapit=='ujin2'): data['ujin2'] = True
#    else:
#        if not (data['zavtrak'] or data['zavtrak2'] or data['obed'] or data['poldnik'] or data['ujin1'] or data['ujin2']):


    return data

def func_read_int(fuchid, fdatpit, flgota='normal', classname='103A', modeldatapit=stolovayainfopit.objects.all().order_by('datapittime')): #Функция ПРОЧИТАТЬ приемы пищи для редактора!
    data = {}
    data['uchid'] = fuchid
    data['datpit'] = fdatpit
    data['falgota'] = flgota
    
    #modelstol1 = modelstol.objects.filter(Q(typeofeda='internat14') | Q(typeofeda='internat59')).order_by('classname','typeofeda','fio')
#    modeldatapit = stolovayainfopit.objects.filter(datapit=fdatpit, uchid_id=fuchid).order_by('-datapittime')
    modeldatapit = list(filter(lambda x:((str(x.datapit)==fdatpit) and (x.uchid_id==int(fuchid))), modeldatapit))
#    modeldatapit = list(filter(lambda x:x.datapit==fdatpit,modeldatapit))
    #data['modeldatapit']=str(modeldatapit)
#            for objm1 in modelstol1:
#                for objpit1 in modeldatapit:
    data['wtf'] = ''
    tmpfdatpit = datetime.strptime(fdatpit,'%Y-%m-%d').date()
    datnumofweek = datetime.strptime(fdatpit,'%Y-%m-%d').weekday()
    if len(modeldatapit) >0 :
        zaglushka = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
        tmpfdatpittime2 = datetime.strptime(fdatpit,'%Y-%m-%d')
        tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
        tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitz = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepito = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitp = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitu1 = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitu2 = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitzg = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        if 1==1:
            for xobj in modeldatapit:
                #data['modelq1'] = xobj
                if xobj.datapit >= tmpdatpit:
                    if tmpfdatpit == xobj.datapit:
                        if xobj.datapittime.timestamp() >= tmpfdatpittime.timestamp():
                            tmpdatpit = xobj.datapit
                            tmpfdatpittime = xobj.datapittime
                            data['zavtrak'] = str(xobj.zavtrak).lower().capitalize() if not(xobj.zavtrak == None) else None
                            data['obed'] = str(xobj.obed).lower().capitalize() if not(xobj.obed == None) else None
                            data['poldnik'] = str(xobj.poldnik).lower().capitalize() if not(xobj.poldnik == None) else None
                            data['ujin1'] = str(xobj.ujin1).lower().capitalize() if not(xobj.ujin1 == None) else None
                            data['ujin2'] = str(xobj.ujin2).lower().capitalize() if not(xobj.ujin2 == None) else None
                            data['obedk'] = str(xobj.obedk).lower().capitalize() if not(xobj.obedk == None) else None
                            data['obedkg1'] = str(xobj.obedkg1).lower().capitalize() if not(xobj.obedkg1 == None) else None
                            data['obedkg2'] = str(xobj.obedkg2).lower().capitalize() if not(xobj.obedkg2 == None) else None
                            data['obedkg3'] = str(xobj.obedkg3).lower().capitalize() if not(xobj.obedkg3 == None) else None
                            data['internatp'] = str(xobj.internatp).lower().capitalize() if not(xobj.internatp == None) else None
                            data['zavtrakg'] = str(xobj.zavtrakg).lower().capitalize() if not(xobj.zavtrakg == None) else None
                            data['datapittime'] = xobj.datapittime
                            #data['wtf'] += str(xobj.datapittime)

    else:
        if flgota == 'internat14' or flgota == 'internat59':
            data['zavtrak'] = "true".lower().capitalize()
            data['obed'] = "true".lower().capitalize()
            data['poldnik'] = "true".lower().capitalize()
            data['ujin1'] = "true".lower().capitalize()
            data['ujin2'] = "true".lower().capitalize()
        if ((flgota == 'lgota14') and (datnumofweek != 5)) :
            data['obedk'] = "true".lower().capitalize()
            #data['zavtrakg'] = "false".lower().capitalize()
        if flgota == 'lgota59':
            data['obedk'] = "true".lower().capitalize()
        if flgota == 'dogovor1':
            data['obedkg1'] =  "true".lower().capitalize()
        if flgota == 'dogovor2':
            data['obedkg2'] =  "true".lower().capitalize()
        if flgota == 'dogovor3':
            data['obedkg3'] =  "true".lower().capitalize()
        if flgota == 'internatp':
            data['internatp'] =  "true".lower().capitalize()

#
#        if datnumofweek != 6 :
#            if flgota == 'lgota59':
#                data['obedk'] = "true".lower().capitalize()
#            if ((flgota == 'lgota14') and (datnumofweek != 5)) :
#                data['obedk'] = "true".lower().capitalize()
#            if flgota == 'dogovor1':
#                data['obedkg1'] =  "true".lower().capitalize()
#            if flgota == 'dogovor2':
#                data['obedkg2'] =  "true".lower().capitalize()
        data['datapittime'] = None
        data['datnumofweek'] = datnumofweek
    return data

#@login_required
def func_read(fuchid, fdatpit, flgota, timestolmodel, modeldatapit, classname='103A', medflag=False): #Функция ПРОЧИТАТЬ приемы пищи для столовой!
    data = {}
#    modelstol5 = modelstol.objects.filter(Q(typeofeda='normal') | Q(typeofeda='kompleks')).order_by('classname','typeofeda','fio')
#    modeldatapit = stolovayainfopit.objects.filter(uchid_id=fuchid).order_by('datapittime')
#    timestolmodel = stolovayapodacha.objects.filter(site=Site.objects.get_current())[:1].get()
    modeldatapit =  list(filter(lambda x:((str(x.datapit)==fdatpit) and (x.uchid_id==int(fuchid))), modeldatapit))#list(filter(lambda x:x.uchid_id==fuchid,modeldatapit))
    zzok=0
    zpok=0
    zook=0
    zu1k=0
    zu2k=0
    zokk=0
    zokkg1=0
    zokkg2=0
    zokkg3=0
    zozg=0

    correctirovka = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
    correctirovka2 = correctirovka
    data['correctirovkaz'] = correctirovka2
    data['correctirovkao'] = correctirovka2
    data['correctirovkap'] = correctirovka2
    data['correctirovkau1'] = correctirovka2
    data['correctirovkau2'] = correctirovka2
    data['correctirovkaok'] = correctirovka2
    data['correctirovkaokg1'] = correctirovka2
    data['correctirovkaokg2'] = correctirovka2
    data['correctirovkaokg3'] = correctirovka2
    data['correctirovkaozg'] = correctirovka2
#    medflag = str(modelstol.objects.filter(id=fuchid).values_list('medflag')[:1].get()[0])
#    medflag = False
#    tmpfdatpit = datetime.strptime(fdatpit,'%Y-%m-%d').date()
#    tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
#    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
#    for objcat in stolovayamedflag.objects.filter(uchid_id=fuchid):
#        if objcat.dateeda >= tmpdatpit:
#            tmpdatpit = objcat.dateeda
#            if tmpfdatpit >= objcat.dateeda :
#                if objcat.datetime1.timestamp() >= tmpfdatpittime.timestamp():
#                    tmpfdatpittime = objcat.datetime1
#                    medflag = objcat.medflag
#    classname = str(modelstol.objects.filter(id=fuchid).values_list('classname')[:1].get()[0])
    tmpfdatpit = datetime.strptime(fdatpit,'%Y-%m-%d').date()
    datnumofweek = datetime.strptime(fdatpit,'%Y-%m-%d').weekday()
    if len(modeldatapit) > 0:
        zaglushka = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
        tmpfdatpittime2 = datetime.strptime(fdatpit,'%Y-%m-%d')
#        tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
#        tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
#        tmpftimepit = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
        tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitz = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepito = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitp = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitu1 = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitu2 = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitok = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitokg1 = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitokg2 = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitokg3 = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitozg = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
#        data['timez']=''
        correctirovkamed = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        correctirovkamed2 = correctirovkamed

        itoffor = {}
        itter = 0
        if ((medflag == 'True') or (flgota in {'internat14','internat59'})):
#        if 1==1 :
            for xobj in modeldatapit:
#                itoffor[itter] = xobj
                if xobj.datapit >= tmpdatpit:
                    tmpdatpit = xobj.datapit
                    if tmpfdatpit == xobj.datapit:
                        if xobj.datapittime.timestamp() >= tmpfdatpittime.timestamp():
                            tmpfdatpittime = xobj.datapittime

                            if isinstance(xobj.forceflagmed, datetime):
                                correctirovkamed = xobj.forceflagmed

                            #zavtrak time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.zavtrak.hour), minute=int(timestolmodel.zavtrak.minute)).timestamp()) or (isinstance(xobj.forceflagz, datetime))) :
                                data['zavtrak'] = str(xobj.zavtrak).lower().capitalize()
                                zzok=1
                                #data['correctirovkaz'] = correctirovka2
                                if isinstance(xobj.forceflagz, datetime):
                                    data['correctirovkaz'] = xobj.forceflagz
                                    if xobj.forceflagz.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflagz
                            elif zzok==0:
                                data['zavtrak'] = "True".lower().capitalize()

                            #obed time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.obed.hour), minute=int(timestolmodel.obed.minute)).timestamp()) or (isinstance(xobj.forceflago, datetime))) :
                                data['obed'] = str(xobj.obed).lower().capitalize()
                                zook=1
                                #data['correctirovkao'] = correctirovka2
                                if isinstance(xobj.forceflago, datetime):
                                    data['correctirovkao'] = xobj.forceflago
                                    if xobj.forceflago.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflago
                            elif zook==0:
                                data['obed'] = "True".lower().capitalize()

                            #poldnik time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.poldnik.hour), minute=int(timestolmodel.poldnik.minute)).timestamp()) or (isinstance(xobj.forceflagp, datetime))) :
                                data['poldnik'] = str(xobj.poldnik).lower().capitalize()
                                zpok=1
                                #data['correctirovkap'] = correctirovka2
                                if isinstance(xobj.forceflagp, datetime):
                                    data['correctirovkap'] = xobj.forceflagp
                                    if xobj.forceflagp.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflagp
                            elif zpok==0:
                                data['poldnik'] = "True".lower().capitalize()

                            #ujin1 time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.ujin1.hour), minute=int(timestolmodel.ujin1.minute)).timestamp()) or (isinstance(xobj.forceflagu1, datetime))) :
                                data['ujin1'] = str(xobj.ujin1).lower().capitalize()
                                zu1k=1
                                #data['correctirovkau1'] = correctirovka2
                                if isinstance(xobj.forceflagu1, datetime):
                                    data['correctirovkau1'] = xobj.forceflagu1
                                    if xobj.forceflagu1.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflagu1
                            elif zu1k==0:
                                data['ujin1'] = "True".lower().capitalize()

                            #ujin2 time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.ujin2.hour), minute=int(timestolmodel.ujin2.minute)).timestamp()) or (isinstance(xobj.forceflagu2, datetime))) :
                                data['ujin2'] = str(xobj.ujin2).lower().capitalize()
                                zu2k=1
                                #data['correctirovkau2'] = correctirovka2
                                if isinstance(xobj.forceflagu2, datetime):
                                    data['correctirovkau2'] = xobj.forceflagu2
                                    if xobj.forceflagu2.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflagu2
                            elif zu2k==0:
                                data['ujin2'] = "True".lower().capitalize()
                            #obedk time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.obedk.hour), minute=int(timestolmodel.obedk.minute)).timestamp()) or (isinstance(xobj.forceflagok, datetime))) :
                                data['obedk'] = str(xobj.obedk).lower().capitalize()
                                zokk=1
                                #data['correctirovkau2'] = correctirovka2
                                if isinstance(xobj.forceflagok, datetime):
                                    data['correctirovkaok'] = xobj.forceflagok
                                    if xobj.forceflagok.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflagok
                            elif zokk==0:
                                data['obedk'] = "False".lower().capitalize()

                            #obedkg1 time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.obedkg1.hour), minute=int(timestolmodel.obedkg1.minute)).timestamp()) or (isinstance(xobj.forceflagokg1, datetime))) :
                                data['obedkg1'] = str(xobj.obedkg1).lower().capitalize()
                                zokkg1=1
                                #data['correctirovkau2'] = correctirovka2
                                if isinstance(xobj.forceflagokg1, datetime):
                                    data['correctirovkaokg1'] = xobj.forceflagokg1
                                    if xobj.forceflagokg1.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflagokg1
                            elif zokkg1==0:
                                data['obedkg1'] = "False".lower().capitalize()

                            #obedkg2 time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.obedkg2.hour), minute=int(timestolmodel.obedkg2.minute)).timestamp()) or (isinstance(xobj.forceflagokg2, datetime))) :
                                data['obedkg2'] = str(xobj.obedkg2).lower().capitalize()
                                zokkg2=1
                                #data['correctirovkau2'] = correctirovka2
                                if isinstance(xobj.forceflagokg2, datetime):
                                    data['correctirovkaokg2'] = xobj.forceflagokg2
                                    if xobj.forceflagokg2.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflagokg2
                            elif zokkg2==0:
                                data['obedkg2'] = "False".lower().capitalize()


                            #obedkg3 time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.obedkg3.hour), minute=int(timestolmodel.obedkg3.minute)).timestamp()) or (isinstance(xobj.forceflagokg3, datetime))) :
                                data['obedkg3'] = str(xobj.obedkg3).lower().capitalize()
                                zokkg3=1
                                #data['correctirovkau2'] = correctirovka2
                                if isinstance(xobj.forceflagokg3, datetime):
                                    data['correctirovkaokg3'] = xobj.forceflagokg3
                                    if xobj.forceflagokg3.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflagokg3
                            elif zokkg3==0:
                                data['obedkg3'] = "False".lower().capitalize()




                            #zavtrakg time test
                            if ((xobj.datapittime.timestamp() <= tmpfdatpittime2.replace(hour=int(timestolmodel.zavtrakg.hour), minute=int(timestolmodel.zavtrakg.minute)).timestamp()) or (isinstance(xobj.forceflagozg, datetime))) :
                                data['zavtrakg'] = str(xobj.zavtrakg).lower().capitalize()
                                zozg=1
                                #data['correctirovkau2'] = correctirovka2
                                if isinstance(xobj.forceflagozg, datetime):
                                    data['correctirovkaozg'] = xobj.forceflagozg
                                    if xobj.forceflagozg.timestamp() > correctirovka.timestamp() :
                                        correctirovka = xobj.forceflagozg
                            elif zozg==0:
                                data['zavtrakg'] = "False".lower().capitalize()

                if (zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) > 0:
                    data['datapit'] = xobj.datapit
                    data['datapittime'] = xobj.datapittime
                    #correctirovka = correctirovka2
                if (zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) == 0:
                    correctirovka = correctirovka2

                if correctirovkamed.timestamp() > correctirovkamed2.timestamp():
                    data['correctirovkamed'] = 1
                itter += 1

    if (correctirovka.timestamp() > correctirovka2.timestamp()):
        data['correctirovka'] = correctirovka
    else:
        #if data['correctirovkaz'].timestamp() == correctirovka2.timestamp():
        if 'correctirovkaz' in data:
            del data['correctirovkaz']
        #if data['correctirovkao'].timestamp() == correctirovka2.timestamp():
        if 'correctirovkao' in data:
            del data['correctirovkao']
        #if data['correctirovkap'].timestamp() == correctirovka2.timestamp():
        if 'correctirovkap' in data:
            del data['correctirovkap']
        #if data['correctirovkau1'].timestamp() == correctirovka2.timestamp():
        if 'correctirovkau1' in data:
            del data['correctirovkau1']
        #if data['correctirovkau2'].timestamp() == correctirovka2.timestamp():
        if 'correctirovkau2' in data:
            del data['correctirovkau2']
        if 'correctirovkaok' in data:
            del data['correctirovkaok']
        if 'correctirovkaokg1' in data:
            del data['correctirovkaokg1']
        if 'correctirovkaokg2' in data:
            del data['correctirovkaokg2']
        if 'correctirovkaokg3' in data:
            del data['correctirovkaokg3']
        if 'correctirovkaozg' in data:
            del data['correctirovkaozg']

        
    if ((flgota == 'internat14' or flgota == 'internat59') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) == 0)):
        data['zavtrak'] = "true".lower().capitalize()
        data['obed'] = "true".lower().capitalize()
        data['poldnik'] = "true".lower().capitalize()
        data['ujin1'] = "true".lower().capitalize()
        data['ujin2'] = "true".lower().capitalize()
    if ((flgota == 'lgota14') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) == 0) and (datnumofweek != 5)):
        data['obedk'] = "true".lower().capitalize()
    if ((flgota == 'lgota59') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) == 0)):
        data['obedk'] = "true".lower().capitalize()
    if ((flgota == 'normal' or flgota == 'dogovor1' or flgota == 'dogovor2' or flgota == 'lgota14') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) == 0) and (classname in mnachalkaclass.keys())):
        data['zavtrak'] = "false".lower().capitalize()
    if ((flgota == 'dogovor1') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) == 0)):
        data['obedkg1'] = "true".lower().capitalize()
    if ((flgota == 'dogovor2') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) == 0)):
        data['obedkg2'] = "true".lower().capitalize()
    if ((flgota == 'dogovor3') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) == 0)):
        data['obedkg3'] = "true".lower().capitalize()
    if ((flgota == 'internatp') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2 + zokkg3 + zozg) == 0)):
        data['internatp'] = "true".lower().capitalize()

#    if datnumofweek != 6 :
#        if ((flgota == 'lgota14') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2) == 0) and (datnumofweek != 5)):
#            data['obedk'] = "true".lower().capitalize()
#        if ((flgota == 'lgota59') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2) == 0)):
#            data['obedk'] = "true".lower().capitalize()
#        if ((flgota == 'normal' or flgota == 'dogovor1' or flgota == 'dogovor2' or flgota == 'lgota14') and ((zzok + zook + zpok + zu1k + zu2k) == 0) and (classname in {'103A','103B','104A','104B'})):
#            data['zavtrak'] = "false".lower().capitalize()
#        if ((flgota == 'dogovor1') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2) == 0)):
#            data['obedkg1'] = "true".lower().capitalize()
#        if ((flgota == 'dogovor2') and ((zzok + zook + zpok + zu1k + zu2k + zokk + zokkg1 + zokkg2) == 0)):
#            data['obedkg2'] = "true".lower().capitalize()
    data['datnumofweek'] = datnumofweek
    return data






@login_required
def AdminViewmemed(request): #EditMED
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['med-ed','stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")


    queryset = modelstol.objects.all().order_by('classname','fio')

    #1
#    lgotaarrlist = queryset.values('typeofeda')
#    list_of_unique_eda = {}#[]
#    unique_eda = sorted(set( val for dic in lgotaarrlist for val in dic.values()))
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))
    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    list_of_unique_class.update({idcl:'Все'})
    idcl=1
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1

#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    selit = selectitems2[0]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")


        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            else:
                selit = selectitems2[0]
            datid = ''
            datchk = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]
            for objdi, objdc in arrdata:
                if datetime.now().timestamp()<(datetime.strptime(datasek,'%Y-%m-%d').replace(hour=9, minute=16)).timestamp():
                    stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                    alertmsg ='Данные ЗАПИСАНЫ Спасибо!'
                else:
                    alertmsg ='Вы пытаетесь ввести данные на сегодняшнюю дату после разрешенного времени(текущая дата 9.15)'


        if dicta.get('form3',0) != 0: #Delete from medcenter
            del dicta['form3']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            datid = ''
            datchk = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[4:],'True')]
                        #modelstol.objects.filter(medflag=True, id=datid[4:]).update(medflag=False)
                        stolovayamedflag(medflag=False, uchid_id=datid[4:], dateeda=datdate[0], datetime1=datetime.now()).save()
                        #stolovayainfodata(datapit=datdate[0],uchid_id=datid[4:], chkflag='False', datazapis=timezone.now()).save()
#                        stolovayainfopit(datapit=datdate[0], uchid_id=datid[4:], zavtrak='True', obed='True', poldnik='True', ujin1='True', ujin2='True', datapittime=datetime.now()).save()
                        #stolovayainfodata.objects.filter(uchid_id=objdi).delete()
                    else:
                        arrdata += [(datid[4:],'False')]
        if dicta.get('form4',0) != 0: #Add to medcenter
            del dicta['form4']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            if dicta.get('fioselect') != 0:
                fioselect = dicta.get('fioselect')[0]
                del dicta['fioselect']
#                modelstol.objects.filter(medflag=False, fio=fioselect).update(medflag=True)
#                fuchid = modelstol.objects.filter(fio=fioselect)[:1].get()
                stolovayamedflag(medflag=True, uchid_id=fioselect, dateeda=datdate[0], datetime1=datetime.now()).save()


#    for qrit in queryset:
#        if qrit.classname == selit:
#            queryset1.append(qrit)
    datamodel1 = []
    datamodel89 = []
    sumuch = 0
    datamodelas = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    stoldiet = set(stolovayadietflag.objects.all())
    modeldatapit=stolovayainfopit.objects.filter(datapit=datasek).order_by('-datapittime')
    for stolm in queryset :

        stolm.medflag = False
        stolm = stolmedflagget(stolm, datasek, stolmed)

        datamodel89.append(stolm)
        if stolm.medflag == False:
            continue

        stolm.dietflag = False
        stolm = stoldietflagget(stolm, datasek, stoldiet)

        stolm.typeofeda = 'normal'
        stolm = stolcategoryget(stolm, datasek, stolcat)

        stolm.chkflag = False
        stolm = stolchkflagget(stolm, datasek, datamodelas)

        stolm.eda = mlgotaarrvseda.copy()
        stolm.eda.update(func_read_int(stolm.id, datasek, stolm.typeofeda, modeldatapit=modeldatapit))
        stolm = setpriemiformatnorm(stolm)

        if str(selit) == 'Все':
            sumuch += 1
            datamodel1.append(stolm)
        else:
            if str(selit) == stolm.classname:
                sumuch += 1
                datamodel1.append(stolm)

    querysetnew = filter(lambda x:x.medflag==False,datamodel89)#modelstol.objects.all().order_by('classname','fio')
    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))
    context = {'queryset':queryset,  'selectitems':selectitems2, 'selit':selit, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0, 'sumuch':sumuch, 'querysetnew':querysetnew}
    return render(request, 'stolovaya/stol-med.html', context)




@login_required
def AdminViewmeblk(request): #EditBLK
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")


    queryset = modelstol.objects.all().order_by('classname','fio')

    #1
#    lgotaarrlist = queryset.values('typeofeda')
#    list_of_unique_eda = {}#[]
#    unique_eda = sorted(set( val for dic in lgotaarrlist for val in dic.values()))
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))
    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    list_of_unique_class.update({idcl:'Все'})
    idcl=1
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1

#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    selit = selectitems2[0]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")


        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            else:
                selit = selectitems2[0]
            datid = ''
            datchk = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]
            for objdi, objdc in arrdata:
                stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                alertmsg ='Данные ЗАПИСАНЫ Спасибо!'


        if dicta.get('form3',0) != 0: #Delete from blklist
            del dicta['form3']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            datid = ''
            datchk = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[4:],'True')]
                        #modelstol.objects.filter(medflag=True, id=datid[4:]).update(medflag=False)
                        stolovayablkdata(blockflag=False, uchid_id=datid[4:], dateeda=datdate[0], datetime1=datetime.now()).save()
                        #stolovayainfodata(datapit=datdate[0],uchid_id=datid[4:], chkflag='False', datazapis=timezone.now()).save()
#                        stolovayainfopit(datapit=datdate[0], uchid_id=datid[4:], zavtrak='True', obed='True', poldnik='True', ujin1='True', ujin2='True', datapittime=datetime.now()).save()
                        #stolovayainfodata.objects.filter(uchid_id=objdi).delete()
                    else:
                        arrdata += [(datid[4:],'False')]
        if dicta.get('form4',0) != 0: #Add to blklist
            del dicta['form4']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            if dicta.get('fioselect') != 0:
                fioselect = dicta.get('fioselect')[0]
                del dicta['fioselect']
#                modelstol.objects.filter(medflag=False, fio=fioselect).update(medflag=True)
#                fuchid = modelstol.objects.filter(fio=fioselect)[:1].get()
                stolovayablkdata(blockflag=True, uchid_id=fioselect, dateeda=datdate[0], datetime1=datetime.now()).save()


#    for qrit in queryset:
#        if qrit.classname == selit:
#            queryset1.append(qrit)
    datamodel1 = []
    datamodel89 = []
    sumuch = 0
    datamodelas = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    stoldiet = set(stolovayadietflag.objects.all())
    modeldatapit=stolovayainfopit.objects.filter(datapit=datasek).order_by('-datapittime')
    datamodelbl = set(stolovayablkdata.objects.all())
    for stolm in queryset :

        stolm.medflag = False
        stolm = stolmedflagget(stolm, datasek, stolmed)

        datamodel89.append(stolm)

        stolm.blockflag = False
        stolm = stolchkblock(stolm, datasek, datamodelbl)

        if stolm.blockflag == False:
            continue

        stolm.dietflag = False
        stolm = stoldietflagget(stolm, datasek, stoldiet)

        stolm.typeofeda = 'normal'
        stolm = stolcategoryget(stolm, datasek, stolcat)

        stolm.chkflag = False
        stolm = stolchkflagget(stolm, datasek, datamodelas)

        stolm.eda = mlgotaarrvseda.copy()
        stolm.eda.update(func_read_int(stolm.id, datasek, stolm.typeofeda, modeldatapit=modeldatapit))
        stolm = setpriemiformatnorm(stolm)

        if str(selit) == 'Все':
            sumuch += 1
            datamodel1.append(stolm)
        else:
            if str(selit) == stolm.classname:
                sumuch += 1
                datamodel1.append(stolm)

    querysetnew = filter(lambda x:x.blockflag==False,datamodel89)#modelstol.objects.all().order_by('classname','fio')
    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))
    context = {'queryset':queryset,  'selectitems':selectitems2, 'selit':selit, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0, 'sumuch':sumuch, 'querysetnew':querysetnew}
    return render(request, 'stolovaya/stol-blk.html', context)





@login_required
def AdminViewmediet(request): #EditDiet
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")


    queryset = modelstol.objects.all().order_by('classname','fio')

    #1
#    lgotaarrlist = queryset.values('typeofeda')
#    list_of_unique_eda = {}#[]
#    unique_eda = sorted(set( val for dic in lgotaarrlist for val in dic.values()))
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))
    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    list_of_unique_class.update({idcl:'Все'})
    idcl=1
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1

#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    selit = selectitems2[0]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")


        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            else:
                selit = selectitems2[0]
            datid = ''
            datchk = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]
            for objdi, objdc in arrdata:
                stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                alertmsg ='Данные ЗАПИСАНЫ Спасибо!'


        if dicta.get('form3',0) != 0: #Delete from dietlist
            del dicta['form3']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            datid = ''
            datchk = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[4:],'True')]
                        #modelstol.objects.filter(medflag=True, id=datid[4:]).update(medflag=False)
                        stolovayadietflag(dietflag=False, uchid_id=datid[4:], dateeda=datdate[0], datetime1=datetime.now()).save()
                        #stolovayainfodata(datapit=datdate[0],uchid_id=datid[4:], chkflag='False', datazapis=timezone.now()).save()
#                        stolovayainfopit(datapit=datdate[0], uchid_id=datid[4:], zavtrak='True', obed='True', poldnik='True', ujin1='True', ujin2='True', datapittime=datetime.now()).save()
                        #stolovayainfodata.objects.filter(uchid_id=objdi).delete()
                    else:
                        arrdata += [(datid[4:],'False')]
        if dicta.get('form4',0) != 0: #Add to dietlist
            del dicta['form4']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            if dicta.get('fioselect') != 0:
                fioselect = dicta.get('fioselect')[0]
                del dicta['fioselect']
#                modelstol.objects.filter(medflag=False, fio=fioselect).update(medflag=True)
#                fuchid = modelstol.objects.filter(fio=fioselect)[:1].get()
                stolovayadietflag(dietflag=True, uchid_id=fioselect, dateeda=datdate[0], datetime1=datetime.now()).save()


#    for qrit in queryset:
#        if qrit.classname == selit:
#            queryset1.append(qrit)
    datamodel1 = []
    datamodel89 = []
    sumuch = 0
    datamodelas = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    stoldiet = set(stolovayadietflag.objects.all())
    modeldatapit=stolovayainfopit.objects.filter(datapit=datasek).order_by('-datapittime')
    #datamodelbl = set(stolovayablkdata.objects.all())
    for stolm in queryset :

        stolm.medflag = False
        stolm = stolmedflagget(stolm, datasek, stolmed)

        datamodel89.append(stolm)

    #    stolm.blockflag = False
    #    stolm = stolchkblock(stolm, datasek, datamodelbl)

    #    if stolm.blockflag == False:
    #        continue

        stolm.dietflag = False
        stolm = stoldietflagget(stolm, datasek, stoldiet)

        if stolm.dietflag == False:
            continue

        stolm.typeofeda = 'normal'
        stolm = stolcategoryget(stolm, datasek, stolcat)

        stolm.chkflag = False
        stolm = stolchkflagget(stolm, datasek, datamodelas)

        stolm.eda = mlgotaarrvseda.copy()
        stolm.eda.update(func_read_int(stolm.id, datasek, stolm.typeofeda, modeldatapit=modeldatapit))
        stolm = setpriemiformatnorm(stolm)

        if str(selit) == 'Все':
            sumuch += 1
            datamodel1.append(stolm)
        else:
            if str(selit) == stolm.classname:
                sumuch += 1
                datamodel1.append(stolm)

    querysetnew = filter(lambda x:x.dietflag==False,datamodel89)#modelstol.objects.all().order_by('classname','fio')
    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))
    context = {'queryset':queryset,  'selectitems':selectitems2, 'selit':selit, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0, 'sumuch':sumuch, 'querysetnew':querysetnew}
    return render(request, 'stolovaya/stol-diet.html', context)




@login_required
def AdminViewmeka(request):
#stol-admin
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)

    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    

    queryset = modelstol.objects.all().order_by('classname','fio')
    #1
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))
    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1
    #1
    lgotaarrlistintl = get_typesofinternat()
    unique_intl = sorted(set( dic for dic,dic2 in lgotaarrlistintl ))
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    list_of_unique_class.update({idcl:'Все'})
    idcl=1
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1

#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    internatarr = modelstol.objects.filter(~Q(internat='normal')).values('internat')
    list_of_unique_int = {}#[]
    unique_int = sorted(set( val for dic in internatarr for val in dic.values()))
    list_of_unique_int.update({'internat':'Все'})
    idcl2=0
    for inter in unique_int:
        if str('stol-admin') in unique_groups:
            list_of_unique_int.update({idcl2:inter[:1]})
            idcl2+=1
        else:
            if str(inter) in unique_groups:
                list_of_unique_int.update({idcl2:inter[:1]})
                idcl2+=1

    selectintitems=list_of_unique_int

#    updatebase=0
    selitint = 'Все'#selectintitems[0]
    selit = selectitems2[1]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('selitint', 0) != 0:
                selitint = dicta.get('selitint')[0]
                del dicta['selitint']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")
        if dicta.get('form9',0) !=0: #del user
            del dicta['form9']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('selitint', 0) != 0:
                selitint = dicta.get('selitint')[0]
                del dicta['selitint']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")
            if dicta.get('uchid',0) != 0:
                uchiddel = dicta.get('uchid')[0]
                if isinstance(uchiddel,int):
                    uchid1=uchiddel
                else:
                    if uchiddel.isdigit():
                        uchid1=int(uchiddel)
                if isinstance(uchid1,int):
                    if len(list(filter(lambda x:x.id==uchid1,queryset))) > 0:
                        modelstol.objects.filter(id=uchid1).update(pitendatedi=datasek)
#        if dicta.get('form9',0) !=0: #tempfunc
#            del dicta['form9']
#            del dicta['csrfmiddlewaretoken']
#            updatebase=1
#            from django.contrib.auth.models import Group, User
#            for itofcl in selectitems2.values():
#                if itofcl == 'Все':
#                    continue
#                user = User.objects.create_user(username=(itofcl+'-ruk'), password=("!"+itofcl+'!d'))
#                user = User.objects.get(username=(itofcl+'-ruk'))
#                new_group, created = Group.objects.get_or_create(name=itofcl)
#                my_group = Group.objects.get(name='class-ed')
#                my_group.user_set.add(user)
#            tmpfdatpit = datetime.strptime(datasek,'%Y-%m-%d').date()
#            tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
#            tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
#            for objcat in modelstol.objects.all().order_by('classname','typeofeda','fio'):
#                stolovayacategory(uchid_id=objcat.id,category=objcat.typeofeda,dateeda=datetime.now().date(),datetime1=datetime.now()).save()





        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker') != 0:
                datdate = dicta.get('datepicker')
                del dicta['datepicker']
                datasek = datdate[0]
            delflag1 = '0'
            if dicta.get('delflag'):
                delflag1 = str(dicta.get('delflag')[0])
                del dicta['delflag']
            delflag1 = 1
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            else:
                selit = selectitems2[0]
            datid = ''
            datchk = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]
            for objdi, objdc in arrdata:
                if delflag1 == '1' or delflag1 == 1:
#                    stolovayainfodata.objects.filter(datapit=datdate[0],uchid_id=objdi).delete()
                    stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
#    for qrit in queryset:
#        if qrit.classname == selit:
#            queryset1.append(qrit)
    datamodel1 = []
    sumuch = 0
    if selitint != 'Все':
        queryset = modelstol.objects.filter(internat=(selitint+'-level')).order_by('classname','fio')
    datamodelas = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    stoldiet = set(stolovayadietflag.objects.all())
    modeldatapit=stolovayainfopit.objects.filter(datapit=datasek).order_by('-datapittime')
    datnumofweek = datetime.strptime(datasek,'%Y-%m-%d').weekday()
    for stolm in queryset :
        stolm.medflag = False
        stolm = stolmedflagget(stolm, datasek, stolmed)

        stolm.dietflag = False
        stolm = stoldietflagget(stolm, datasek, stoldiet)

        stolm.typeofeda = 'normal'
        stolm = stolcategoryget(stolm, datasek, stolcat)

#        if not((stolm.typeofeda == 'internat14') or (stolm.typeofeda == 'internat59')):
#            continue
        flagdata=0
        stolm.eda = mlgotaarrvseda.copy()
        if not hasattr(stolm, 'datazapis'):
#            if not ((stolm.classname == '1XKO') and (datnumofweek == 2)):
            ##################KOSTIL################################
#            if not ((stolm.classname == '103A') and (stolm.typeofeda != 'internat14') and (datnumofweek == 5)):
            if 1==1:
            ##################KOSTIL################################
                if not(not((stolm.typeofeda == 'internat14') or (stolm.typeofeda == 'internat59') or (stolm.typeofeda == 'internatp')) and (datnumofweek == 6)):
                    stolm.eda.update(func_read_int(stolm.id, datasek, stolm.typeofeda, modeldatapit=modeldatapit))

#        stolm.eda.update(func_read_int(stolm.id, datasek, stolm.typeofeda, modeldatapit=modeldatapit))
        tmpfdatpit = datetime.strptime(datasek,'%Y-%m-%d').date()
        tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)

        stolm.chkflag = False
        stolm = stolchkflagget(stolm, datasek, datamodelas)

        if str(selit) == 'Все':
            sumuch += 1
            datamodel1.append(stolm)
        else:
            if str(selit) == stolm.classname:
                sumuch += 1
                datamodel1.append(stolm)
    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))
    context = {'queryset':queryset,  'selectitems':selectitems2, 'selit':selit, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0, 'sumuch':sumuch, 'selectintitems':selectintitems, 'selitint':selitint, 'unique_eda':unique_eda, 'unique_class':unique_class, 'unique_intl':unique_intl}
    return render(request, 'stolovaya/stol-adminka.html', context)

@login_required
def form_test3(request, *args, **kwargs): #Обработчк от изменения льготы СОХРАНИТЬ!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['uchid'] = dicta.get('uchid')[0]
            data['datpit'] = dicta.get('datpit')[0]
            data['lgota'] = dicta.get('lgota')[0]
            data['saveflag'] = dicta.get('saveflag')[0]
#            stolovayainfopit.objects.filter(datapit=data['datpit'], uchid_id=data['uchid']).delete()
            if data['saveflag'] == 'ok':
                stolovayacategory(dateeda=data['datpit'], uchid_id=data['uchid'], category=data['lgota'], datetime1=datetime.now()).save()
                data['success'] = 'ok'
    context = {'data':data}
    return JsonResponse(data)

@login_required
def form_test4(request, *args, **kwargs): #Обработчк от изменения класса СОХРАНИТЬ!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['uchid'] = dicta.get('uchid')[0]
            data['saveflag'] = dicta.get('saveflag')[0]
            data['classn'] = dicta.get('classn')[0]
#            stolovayainfopit.objects.filter(datapit=data['datpit'], uchid_id=data['uchid']).delete()
            if data['saveflag'] == 'ok':
                modelstol.objects.filter(id=data['uchid']).update(classname=data['classn'])
                data['success'] = 'ok'
    context = {'data':data}
    return JsonResponse(data)

@login_required
def form_test5(request, *args, **kwargs): #Обработчк от изменения ФИО СОХРАНИТЬ!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}
#    dicta = dict(request.GET)
#    data['uchid'] = dicta.get('uchid')[0]
#    data['uchn'] = dicta.get('uchn')[0]
#    data['saveflag'] = dicta.get('saveflag')[0]
#    data['go']='go'

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['uchid'] = dicta.get('uchid')[0]
            data['uchn'] = dicta.get('uchn')[0]
            data['saveflag'] = dicta.get('saveflag')[0]
            if data['saveflag'] == 'ok':
                modelstol.objects.filter(id=data['uchid']).update(fio=data['uchn'])
                data['success'] = 'ok'
    context = {'data':data}
    return JsonResponse(data)

@login_required
def form_test6(request, *args, **kwargs): #Обработчк от изменения Этажа интерната СОХРАНИТЬ!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}
#    dicta = dict(request.GET)
#    data['uchid'] = dicta.get('uchid')[0]
#    data['uchn'] = dicta.get('uchn')[0]
#    data['saveflag'] = dicta.get('saveflag')[0]
#    data['go']='go'

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['uchid'] = dicta.get('uchid')[0]
            data['intl'] = dicta.get('intl')[0]
            data['saveflag'] = dicta.get('saveflag')[0]
            if data['saveflag'] == 'ok':
                modelstol.objects.filter(id=data['uchid']).update(internat=data['intl'])
                data['success'] = 'ok'
    context = {'data':data}
    return JsonResponse(data)


@login_required
def form_test7(request, *args, **kwargs): #Обработчк Создать нового СОХРАНИТЬ!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['clname'] = dicta.get('clname')[0]
            data['uchfio'] = dicta.get('uchfio')[0]
            data['lgotan'] = dicta.get('lgotan')[0]
            data['intl'] = dicta.get('intl')[0]
            data['datel'] = dicta.get('datel')[0]
            data['saveflag'] = dicta.get('saveflag')[0]
            if data['saveflag'] == 'ok':
                nmodstol = modelstol.objects.create(classname=data['clname'], fio=data['uchfio'], internat=data['intl'], pitendateen=data['datel'])
                data['nmodstol']=nmodstol.id
                ncatstol = stolovayacategory.objects.create(dateeda=data['datel'],category=data['lgotan'],uchid_id=nmodstol.id, datetime1=datetime.now())
                data['ncatstol']=ncatstol.id
                data['success'] = 'ok'
    context = {'data':data}
    return JsonResponse(data)

@login_required
def form_testf(request, *args, **kwargs): #Обработчк от изменения режима питания принуд СОХРАНИТЬ!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-view','stol-admin','int-ed', 'class-ed']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['uchid'] = dicta.get('uchid')[0]
            data['datpit'] = dicta.get('datpit')[0]
            data['zavtrak'] =  dicta.get('zavtrak')[0].lower().capitalize() if not(dicta.get('zavtrak', None) is None) else None
            data['obed'] = dicta.get('obed')[0].lower().capitalize() if not(dicta.get('obed', None) is None) else None #dicta.get('obed')[0].lower().capitalize()
            data['poldnik'] = dicta.get('poldnik')[0].lower().capitalize() if not(dicta.get('poldnik', None) is None) else None #dicta.get('poldnik')[0].lower().capitalize()
            data['ujin1'] = dicta.get('ujin1')[0].lower().capitalize() if not(dicta.get('ujin1', None) is None) else None #dicta.get('ujin1')[0].lower().capitalize()
            data['ujin2'] = dicta.get('ujin2')[0].lower().capitalize() if not(dicta.get('ujin2', None) is None) else None #dicta.get('ujin2')[0].lower().capitalize()
            data['obedk'] = dicta.get('obedk')[0].lower().capitalize() if not(dicta.get('obedk', None) is None) else None #dicta.get('obedk')[0].lower().capitalize()
            data['obedkg1'] = dicta.get('obedkg1')[0].lower().capitalize() if not(dicta.get('obedkg1', None) is None) else None #dicta.get('obedkg1')[0].lower().capitalize()
            data['obedkg2'] = dicta.get('obedkg2')[0].lower().capitalize() if not(dicta.get('obedkg2', None) is None) else None #dicta.get('obedkg2')[0].lower().capitalize()
            data['obedkg3'] = dicta.get('obedkg3')[0].lower().capitalize() if not(dicta.get('obedkg3', None) is None) else None #dicta.get('obedkg3')[0].lower().capitalize()
            data['internatp'] = dicta.get('internatp')[0].lower().capitalize() if not(dicta.get('internatp', None) is None) else None #dicta.get('obedkg3')[0].lower().capitalize()
            data['zavtrakg'] = dicta.get('zavtrakg')[0].lower().capitalize() if not(dicta.get('zavtrakg', None) is None) else None #dicta.get('obedkg2')[0].lower().capitalize()
            #stolovayainfopit.objects.filter(datapit=data['datpit'], uchid_id=data['uchid']).delete()
            stolovayainfopit(datapit=data['datpit'], uchid_id=data['uchid'], zavtrak=data['zavtrak'], obed=data['obed'], poldnik=data['poldnik'], ujin1=data['ujin1'], ujin2=data['ujin2'], obedk=data['obedk'], obedkg1=data['obedkg1'], obedkg2=data['obedkg2'], obedkg3=data['obedkg3'], zavtrakg=data['zavtrakg'], internatp=data['internatp'] , datapittime=datetime.now(),forceflago=datetime.now(),forceflagp=datetime.now(),forceflagz=datetime.now(),forceflagu1=datetime.now(),forceflagu2=datetime.now(), forceflagok=datetime.now(), forceflagokg1=datetime.now(), forceflagokg2=datetime.now(), forceflagokg3=datetime.now(), forceflagozg=datetime.now() ).save()
            data['success'] = 'ok'
    context = {'data':data}
    return JsonResponse(data)

@login_required
def AdminViewmeKor(request): #корректировка для сведения отчета
#stol-admin
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin','stol-correct']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)

    dateminmax = [0,1]
    dateminmax[0]=(datetime.now()+timedelta(days=-4)).strftime("%Y-%m-%d")
    dateminmax[1]=datetime.now().strftime("%Y-%m-%d")

    queryset = modelstol.objects.all().order_by('classname','fio')
    #1
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))
    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    list_of_unique_class.update({idcl:'Все'})
    idcl=1
    list_of_unique_class.update({idcl:'Началка_льготники'})
    idcl=2
    list_of_unique_class.update({idcl:'Старшие_льготники'})
    idcl=3
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1

    selectitems2 = list_of_unique_class
    #2
    internatarr = modelstol.objects.filter(~Q(internat='normal')).values('internat')
    list_of_unique_int = {}#[]
    unique_int = sorted(set( val for dic in internatarr for val in dic.values()))
    list_of_unique_int.update({'internat':'Все'})
    idcl2=0
    for inter in unique_int:
        if str('stol-admin') in unique_groups:
            list_of_unique_int.update({idcl2:inter[:1]})
            idcl2+=1
        else:
            if str(inter) in unique_groups:
                list_of_unique_int.update({idcl2:inter[:1]})
                idcl2+=1

    selectintitems=list_of_unique_int


    selitint = 'Все'#selectintitems[0]
    selit = selectitems2[1]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('selitint', 0) != 0:
                selitint = dicta.get('selitint')[0]
                del dicta['selitint']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")






    datamodel1 = []
    sumuch = 0
    if selitint != 'Все':
        queryset = modelstol.objects.filter(internat=(selitint+'-level'), medflag=False).order_by('classname','fio')
    datamodelas = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    nachalkaclass = mnachalkaclass.copy()
    lgotnikilistnach = mlgotnikilistnach.copy()
    lgotnikilistbol = mlgotnikilistbol.copy()
    queryset=queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    stoldiet = set(stolovayadietflag.objects.all())
    edachk = mlgotaarrvseda.keys()#['zavtrak','obed','poldnik', 'ujin1', 'ujin2', 'zavtrakg', 'obedk','obedkg1', 'obedkg2']
    modeldatapitaf=set(stolovayainfopitafter.objects.filter(datapit=datasek).order_by('-datapittime'))
    modeldatapit=set(stolovayainfopit.objects.filter(datapit=datasek).order_by('-datapittime'))
    datnumofweek = datetime.strptime(datasek,'%Y-%m-%d').weekday()
    qrcodesbase = stolovayafactstol.objects.filter(dateeda=datasek)
    for stolm in queryset :
        stolm.medflag = False
        stolm = stolmedflagget(stolm, datasek, stolmed)

        stolm.dietflag = False
        stolm = stoldietflagget(stolm, datasek, stoldiet)

        stolm.typeofeda = 'normal'
        stolm = stolcategoryget(stolm, datasek, stolcat)

        stolm.chkflag = False
        stolm = stolchkflagget(stolm, datasek, datamodelas)

        stolm.eda = mlgotaarrvseda.copy()
        stolm.eda2 = mlgotaarrvseda.copy()
        stolm.eda9 = medaqr.copy()
        stolm.eda3 = {}
        if 1==1:
#        if not hasattr(stolm, 'datazapis'):
#            if not ((stolm.classname == '1XKO') and (datnumofweek == 2)):
            ##################KOSTIL################################
#            if not ((stolm.classname == '103A') and (stolm.typeofeda != 'internat14') and (datnumofweek == 5)):
            if 1==1:
            ##################KOSTIL################################
                if not(not((stolm.typeofeda == 'internat14') or (stolm.typeofeda == 'internat59') or (stolm.typeofeda == 'internatp')) and (datnumofweek == 6)):
                    stolm.eda.update(func_read_int(stolm.id, datasek, stolm.typeofeda, modeldatapit=modeldatapit))
                    stolm.eda3 = func_read_int_fact(stolm.id, datasek, stolm.typeofeda, modeldatapit=modeldatapitaf)


        if set(edachk).intersection(set(stolm.eda3)):
            stolm.eda2.update(stolm.eda3)
        else:
            stolm.eda2 = stolm.eda.copy()
        stolm=setpriemiformat(stolm)

        tmpfdatpit = datetime.strptime(datasek,'%Y-%m-%d').date()
        tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)

        if (stolm.chkflag == True or stolm.chkflag == 'True'):
            for i,x in stolm.eda.items(): 
                if x == 'True' or x == True :
                    stolm.eda[i]=False
            if set(stolm.eda2) != set(stolm.eda3):
                for i,x in stolm.eda2.items(): 
                    if x == 'True' or x == True :
                        stolm.eda2[i]=False


        if str(selit) == 'Все':
            sumuch += 1
            datamodel1.append(stolm)
        elif str(selit) == 'Началка_льготники':
            if (stolm.classname in nachalkaclass):
                if not(stolm.typeofeda in lgotnikilistnach):
                    continue
                sumuch += 1
                datamodel1.append(stolm)
        elif str(selit) == 'Старшие_льготники':
            if not(stolm.classname in nachalkaclass):
                if not(stolm.typeofeda in lgotnikilistbol):
                    continue
                sumuch += 1
                datamodel1.append(stolm)
        else:
            if str(selit) == stolm.classname:
                sumuch += 1
                datamodel1.append(stolm)
        stolm.eda9.update(func_read_qr(stolm.id, datasek, qrcodesbase=qrcodesbase))
    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))
    context = {'queryset':queryset,  'selectitems':selectitems2, 'selit':selit, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0, 'sumuch':sumuch, 'selectintitems':selectintitems, 'selitint':selitint, 'unique_eda':unique_eda, 'unique_class':unique_class}
    return render(request, 'stolovaya/stol-correct.html', context)

def setpriemiformat(stolm):
    edachk = mlgotaarrvseda.keys()
    nachalkaclass = mnachalkaclass.copy()
    lgotnikilistnach = mlgotnikilistnach.copy()
    lgotnikilistbol = mlgotnikilistbol.copy()

    if stolm.typeofeda == 'normal':
        if not(stolm.classname in nachalkaclass):
            stolm.eda.pop('zavtrakg')
            stolm.eda2.pop('zavtrakg')
        stolm.eda.pop('zavtrak')
        stolm.eda2.pop('zavtrak')
        stolm.eda.pop('obed')
        stolm.eda.pop('poldnik')
        stolm.eda.pop('ujin1')
        stolm.eda.pop('ujin2')
        stolm.eda.pop('obedk')
        stolm.eda2.pop('obed')
        stolm.eda2.pop('poldnik')
        stolm.eda2.pop('ujin1')
        stolm.eda2.pop('ujin2')
        stolm.eda2.pop('obedk')
        stolm.eda2.pop('obedkg1')
        stolm.eda2.pop('obedkg2')
        stolm.eda.pop('obedkg1')
        stolm.eda.pop('obedkg2')
        stolm.eda.pop('obedkg3')
        stolm.eda2.pop('obedkg3')
        stolm.eda.pop('internatp')
        stolm.eda2.pop('internatp')
    if stolm.typeofeda == 'lgota14':
        stolm.eda.pop('zavtrak')
        stolm.eda2.pop('zavtrak')
        stolm.eda.pop('obed')
        stolm.eda.pop('poldnik')
        stolm.eda.pop('ujin1')
        stolm.eda.pop('ujin2')
        #stolm.eda.pop('obedk')
        stolm.eda2.pop('obed')
        stolm.eda2.pop('poldnik')
        stolm.eda2.pop('ujin1')
        stolm.eda2.pop('ujin2')
        stolm.eda2.pop('obedkg1')
        stolm.eda2.pop('obedkg2')
        stolm.eda.pop('obedkg1')
        stolm.eda.pop('obedkg2')
        stolm.eda.pop('obedkg3')
        stolm.eda2.pop('obedkg3')
        stolm.eda.pop('internatp')
        stolm.eda2.pop('internatp')
    if stolm.typeofeda == 'lgota59':
        stolm.eda.pop('zavtrakg')
        stolm.eda2.pop('zavtrakg')
        stolm.eda.pop('zavtrak')
        stolm.eda.pop('obed')
        stolm.eda.pop('poldnik')
        stolm.eda.pop('ujin1')
        stolm.eda.pop('ujin2')
        #stolm.eda.pop('obedk')
        stolm.eda2.pop('zavtrak')
        stolm.eda2.pop('obed')
        stolm.eda2.pop('poldnik')
        stolm.eda2.pop('ujin1')
        stolm.eda2.pop('ujin2')
        stolm.eda2.pop('obedkg1')
        stolm.eda2.pop('obedkg2')
        stolm.eda.pop('obedkg1')
        stolm.eda.pop('obedkg2')
        stolm.eda.pop('obedkg3')
        stolm.eda2.pop('obedkg3')
        stolm.eda.pop('internatp')
        stolm.eda2.pop('internatp')
    if ((stolm.typeofeda == 'internat14') or (stolm.typeofeda == 'internat59')):
        #stolm.eda.pop('zavtrak')
        #stolm.eda.pop('obed')
        #stolm.eda.pop('poldnik')
        #stolm.eda.pop('ujin1')
        #stolm.eda.pop('ujin2')
        stolm.eda.pop('zavtrakg')
        stolm.eda2.pop('zavtrakg')
        stolm.eda.pop('obedk')
        stolm.eda2.pop('obedk')
        stolm.eda2.pop('obedkg1')
        stolm.eda2.pop('obedkg2')
        stolm.eda.pop('obedkg1')
        stolm.eda.pop('obedkg2')
        stolm.eda.pop('obedkg3')
        stolm.eda2.pop('obedkg3')
        stolm.eda.pop('internatp')
        stolm.eda2.pop('internatp')
    if stolm.typeofeda == 'dogovor1':
        if not(stolm.classname in nachalkaclass):
            stolm.eda.pop('zavtrakg')
            stolm.eda2.pop('zavtrakg')
        #stolm.eda.pop('zavtrak')
        stolm.eda.pop('zavtrak')
        stolm.eda2.pop('zavtrak')
        stolm.eda.pop('obed')
        stolm.eda.pop('poldnik')
        stolm.eda.pop('ujin1')
        stolm.eda.pop('ujin2')
        stolm.eda.pop('obedk')
        stolm.eda2.pop('obedk')
        #stolm.eda2.pop('zavtrak')
        stolm.eda2.pop('obed')
        stolm.eda2.pop('poldnik')
        stolm.eda2.pop('ujin1')
        stolm.eda2.pop('ujin2')
        #stolm.eda2.pop('obedkg1')
        stolm.eda2.pop('obedkg2')
        #stolm.eda.pop('obedkg1')
        stolm.eda.pop('obedkg2')
        stolm.eda.pop('obedkg3')
        stolm.eda2.pop('obedkg3')
        stolm.eda.pop('internatp')
        stolm.eda2.pop('internatp')
    if stolm.typeofeda == 'dogovor2':
        if not(stolm.classname in nachalkaclass):
            stolm.eda.pop('zavtrakg')
            stolm.eda2.pop('zavtrakg')
        #stolm.eda.pop('zavtrak')
        stolm.eda.pop('zavtrak')
        stolm.eda2.pop('zavtrak')
        stolm.eda.pop('obed')
        stolm.eda.pop('poldnik')
        stolm.eda.pop('ujin1')
        stolm.eda.pop('ujin2')
        stolm.eda.pop('obedk')
        stolm.eda2.pop('obedk')
        #stolm.eda2.pop('zavtrak')
        stolm.eda2.pop('obed')
        stolm.eda2.pop('poldnik')
        stolm.eda2.pop('ujin1')
        stolm.eda2.pop('ujin2')
        stolm.eda2.pop('obedkg1')
        #stolm.eda2.pop('obedkg2')
        stolm.eda.pop('obedkg1')
        stolm.eda.pop('obedkg3')
        stolm.eda2.pop('obedkg3')
        #stolm.eda.pop('obedkg2')
        stolm.eda.pop('internatp')
        stolm.eda2.pop('internatp')
    if stolm.typeofeda == 'dogovor3':
        if not(stolm.classname in nachalkaclass):
            stolm.eda.pop('zavtrakg')
            stolm.eda2.pop('zavtrakg')
        #stolm.eda.pop('zavtrak')
        stolm.eda.pop('zavtrak')
        stolm.eda2.pop('zavtrak')
        stolm.eda.pop('obed')
        stolm.eda.pop('poldnik')
        stolm.eda.pop('ujin1')
        stolm.eda.pop('ujin2')
        stolm.eda.pop('obedk')
        stolm.eda2.pop('obedk')
        #stolm.eda2.pop('zavtrak')
        stolm.eda2.pop('obed')
        stolm.eda2.pop('poldnik')
        stolm.eda2.pop('ujin1')
        stolm.eda2.pop('ujin2')
        stolm.eda2.pop('obedkg1')
        stolm.eda2.pop('obedkg2')
        stolm.eda.pop('obedkg1')
        #stolm.eda.pop('obedkg3')
        stolm.eda.pop('obedkg2')
        stolm.eda.pop('internatp')
        stolm.eda2.pop('internatp')
    if stolm.typeofeda == 'internatp':
        if not(stolm.classname in nachalkaclass):
            stolm.eda.pop('zavtrakg')
            stolm.eda2.pop('zavtrakg')
        #stolm.eda.pop('zavtrak')
        stolm.eda.pop('zavtrak')
        stolm.eda2.pop('zavtrak')
        stolm.eda.pop('obed')
        stolm.eda.pop('poldnik')
        stolm.eda.pop('ujin1')
        stolm.eda.pop('ujin2')
        stolm.eda.pop('obedk')
        stolm.eda2.pop('obedk')
        #stolm.eda2.pop('zavtrak')
        stolm.eda2.pop('obed')
        stolm.eda2.pop('poldnik')
        stolm.eda2.pop('ujin1')
        stolm.eda2.pop('ujin2')
        stolm.eda2.pop('obedkg1')
        stolm.eda2.pop('obedkg2')
        stolm.eda2.pop('obedkg3')
        stolm.eda.pop('obedkg1')
        stolm.eda.pop('obedkg3')
        stolm.eda.pop('obedkg2')


    if not(set(edachk).intersection(set(stolm.eda))):
        stolm.eda.clear()
    if not(set(edachk).intersection(set(stolm.eda2))):
        stolm.eda2.clear()
    return stolm

def setpriemiformatnorm(stolm):
    edachk = mlgotaarrvseda.keys()
    nachalkaclass = mnachalkaclass.copy()
    lgotnikilistnach = mlgotnikilistnach.copy()
    lgotnikilistbol = mlgotnikilistbol.copy()

    if stolm.typeofeda == 'normal':
        if not(stolm.classname in nachalkaclass):
            if 'zavtrakg' in stolm.eda :stolm.eda.pop('zavtrakg')
        if 'zavtrak' in stolm.eda :stolm.eda.pop('zavtrak')
        if 'obed' in stolm.eda :stolm.eda.pop('obed')
        if 'poldnik' in stolm.eda :stolm.eda.pop('poldnik')
        if 'ujin1' in stolm.eda :stolm.eda.pop('ujin1')
        if 'ujin2' in stolm.eda :stolm.eda.pop('ujin2')
        if 'obedk' in stolm.eda :stolm.eda.pop('obedk')
        if 'obedkg1' in stolm.eda :stolm.eda.pop('obedkg1')
        if 'obedkg2' in stolm.eda :stolm.eda.pop('obedkg2')
        if 'obedkg3' in stolm.eda :stolm.eda.pop('obedkg3')
        if 'internatp' in stolm.eda :stolm.eda.pop('internatp')
    if stolm.typeofeda == 'lgota14':
        if 'zavtrak' in stolm.eda :stolm.eda.pop('zavtrak')
        if 'obed' in stolm.eda :stolm.eda.pop('obed')
        if 'poldnik' in stolm.eda :stolm.eda.pop('poldnik')
        if 'ujin1' in stolm.eda :stolm.eda.pop('ujin1')
        if 'ujin2' in stolm.eda :stolm.eda.pop('ujin2')
        if 'obedkg1' in stolm.eda :stolm.eda.pop('obedkg1')
        if 'obedkg2' in stolm.eda :stolm.eda.pop('obedkg2')
        if 'obedkg3' in stolm.eda :stolm.eda.pop('obedkg3')
        if 'internatp' in stolm.eda :stolm.eda.pop('internatp')
    if stolm.typeofeda == 'lgota59':
        if 'zavtrakg' in stolm.eda :stolm.eda.pop('zavtrakg')
        if 'zavtrak' in stolm.eda :stolm.eda.pop('zavtrak')
        if 'obed' in stolm.eda :stolm.eda.pop('obed')
        if 'poldnik' in stolm.eda :stolm.eda.pop('poldnik')
        if 'ujin1' in stolm.eda :stolm.eda.pop('ujin1')
        if 'ujin2' in stolm.eda :stolm.eda.pop('ujin2')
        if 'obedkg1' in stolm.eda :stolm.eda.pop('obedkg1')
        if 'obedkg2' in stolm.eda :stolm.eda.pop('obedkg2')
        if 'obedkg3' in stolm.eda :stolm.eda.pop('obedkg3')
        if 'internatp' in stolm.eda :stolm.eda.pop('internatp')
    if ((stolm.typeofeda == 'internat14') or (stolm.typeofeda == 'internat59')):
        if 'zavtrakg' in stolm.eda : stolm.eda.pop('zavtrakg')
        if 'obedk' in stolm.eda : stolm.eda.pop('obedk')
        if 'obedkg1' in stolm.eda : stolm.eda.pop('obedkg1')
        if 'obedkg2' in stolm.eda : stolm.eda.pop('obedkg2')
        if 'obedkg3' in stolm.eda : stolm.eda.pop('obedkg3')
        if 'internatp' in stolm.eda : stolm.eda.pop('internatp')
    if stolm.typeofeda == 'dogovor1':
        if not(stolm.classname in nachalkaclass):
            if 'zavtrakg' in stolm.eda : stolm.eda.pop('zavtrakg')
        if 'zavtrak' in stolm.eda : stolm.eda.pop('zavtrak')
        if 'obed' in stolm.eda : stolm.eda.pop('obed')
        if 'poldnik' in stolm.eda : stolm.eda.pop('poldnik')
        if 'ujin1' in stolm.eda : stolm.eda.pop('ujin1')
        if 'ujin2' in stolm.eda : stolm.eda.pop('ujin2')
        if 'obedk' in stolm.eda : stolm.eda.pop('obedk')
        if 'obedkg2' in stolm.eda : stolm.eda.pop('obedkg2')
        if 'obedkg3' in stolm.eda : stolm.eda.pop('obedkg3')
        if 'internatp' in stolm.eda : stolm.eda.pop('internatp')
    if stolm.typeofeda == 'dogovor2':
        if not(stolm.classname in nachalkaclass):
            if 'zavtrakg' in stolm.eda : stolm.eda.pop('zavtrakg')
        if 'zavtrak' in stolm.eda : stolm.eda.pop('zavtrak')
        if 'obed' in stolm.eda : stolm.eda.pop('obed')
        if 'poldnik' in stolm.eda : stolm.eda.pop('poldnik')
        if 'ujin1' in stolm.eda : stolm.eda.pop('ujin1')
        if 'ujin2' in stolm.eda : stolm.eda.pop('ujin2')
        if 'obedk' in stolm.eda : stolm.eda.pop('obedk')
        if 'obedkg1' in stolm.eda : stolm.eda.pop('obedkg1')
        if 'obedkg3' in stolm.eda : stolm.eda.pop('obedkg3')
        if 'internatp' in stolm.eda : stolm.eda.pop('internatp')
    if stolm.typeofeda == 'dogovor3':
        if not(stolm.classname in nachalkaclass):
            if 'zavtrakg' in stolm.eda : stolm.eda.pop('zavtrakg')
        if 'zavtrak' in stolm.eda : stolm.eda.pop('zavtrak')
        if 'obed' in stolm.eda : stolm.eda.pop('obed')
        if 'poldnik' in stolm.eda : stolm.eda.pop('poldnik')
        if 'ujin1' in stolm.eda : stolm.eda.pop('ujin1')
        if 'ujin2' in stolm.eda : stolm.eda.pop('ujin2')
        if 'obedk' in stolm.eda : stolm.eda.pop('obedk')
        if 'obedkg1' in stolm.eda : stolm.eda.pop('obedkg1')
        if 'obedkg2' in stolm.eda : stolm.eda.pop('obedkg2')
        if 'internatp' in stolm.eda : stolm.eda.pop('internatp')
    if stolm.typeofeda == 'internatp':
        if not(stolm.classname in nachalkaclass):
            if 'zavtrakg' in stolm.eda : stolm.eda.pop('zavtrakg')
        if 'zavtrak' in stolm.eda : stolm.eda.pop('zavtrak')
        if 'obed' in stolm.eda : stolm.eda.pop('obed')
        if 'poldnik' in stolm.eda : stolm.eda.pop('poldnik')
        if 'ujin1' in stolm.eda : stolm.eda.pop('ujin1')
        if 'ujin2' in stolm.eda : stolm.eda.pop('ujin2')
        if 'obedk' in stolm.eda : stolm.eda.pop('obedk')
        if 'obedkg1' in stolm.eda : stolm.eda.pop('obedkg1')
        if 'obedkg2' in stolm.eda : stolm.eda.pop('obedkg2')
        if 'obedkg3' in stolm.eda : stolm.eda.pop('obedkg3')

    if not(set(edachk).intersection(set(stolm.eda))):
        stolm.eda.clear()
    return stolm

def func_read_int_fact(fuchid, fdatpit, flgota='normal', classname='103A', modeldatapit=stolovayainfopitafter.objects.all().order_by('-datapittime')): #Функция ПРОЧИТАТЬ приемы пищи для редактора!
    data = {}
    data['uchid'] = fuchid
    data['datpit'] = fdatpit
    #modelstol1 = modelstol.objects.filter(Q(typeofeda='internat14') | Q(typeofeda='internat59')).order_by('classname','typeofeda','fio')
    #modeldatapit = stolovayainfopitafter.objects.filter(datapit=fdatpit, uchid_id=fuchid).order_by('-datapittime')
    modeldatapit = list(filter(lambda x:((str(x.datapit)==fdatpit) and (x.uchid_id==int(fuchid))), modeldatapit))
#            for objm1 in modelstol1:
#                for objpit1 in modeldatapit:
    if len(modeldatapit) > 0 :
        tmpfdatpit = datetime.strptime(fdatpit,'%Y-%m-%d').date()
        zaglushka = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
        tmpfdatpittime2 = datetime.strptime(fdatpit,'%Y-%m-%d')
        tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
        tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitz = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepito = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitp = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitu1 = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitu2 = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        tmpftimepitzg = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        if 1==1:
            for xobj in modeldatapit:
                if xobj.datapit >= tmpdatpit:
                    if tmpfdatpit == xobj.datapit:
                        if xobj.datapittime.timestamp() >= tmpfdatpittime.timestamp():
                            tmpdatpit = xobj.datapit
                            tmpfdatpittime = xobj.datapittime
                            data['zavtrak'] = str(xobj.zavtrak).lower().capitalize()
                            data['obed'] = str(xobj.obed).lower().capitalize()
                            data['poldnik'] = str(xobj.poldnik).lower().capitalize()
                            data['ujin1'] = str(xobj.ujin1).lower().capitalize()
                            data['ujin2'] = str(xobj.ujin2).lower().capitalize()
                            data['obedk'] = str(xobj.obedk).lower().capitalize()
                            data['obedkg1'] = str(xobj.obedkg1).lower().capitalize()
                            data['obedkg2'] = str(xobj.obedkg2).lower().capitalize()
                            data['obedkg3'] = str(xobj.obedkg3).lower().capitalize()
                            data['internatp'] = str(xobj.internatp).lower().capitalize()
                            data['zavtrakg'] = str(xobj.zavtrakg).lower().capitalize()
                            data['datapittime'] = xobj.datapittime

    return data

@login_required
def form_testfkor(request, *args, **kwargs): #Обработчк от изменения режима питания принуд СОХРАНИТЬ!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin','stol-correct']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['uchid'] = dicta.get('uchid')[0]
            data['datpit'] = dicta.get('datpit')[0]
#            data['zavtrak'] = dicta.get('zavtrak')[0].lower().capitalize()
#            data['obed'] = dicta.get('obed')[0].lower().capitalize()
#            data['poldnik'] = dicta.get('poldnik')[0].lower().capitalize()
#            data['ujin1'] = dicta.get('ujin1')[0].lower().capitalize()
#            data['ujin2'] = dicta.get('ujin2')[0].lower().capitalize()
#            data['obedk'] = dicta.get('obedk')[0].lower().capitalize()
            data['zavtrak'] =  dicta.get('zavtrak')[0].lower().capitalize() if not(dicta.get('zavtrak', None) is None) else None
            data['obed'] = dicta.get('obed')[0].lower().capitalize() if not(dicta.get('obed', None) is None) else None #dicta.get('obed')[0].lower().capitalize()
            data['poldnik'] = dicta.get('poldnik')[0].lower().capitalize() if not(dicta.get('poldnik', None) is None) else None #dicta.get('poldnik')[0].lower().capitalize()
            data['ujin1'] = dicta.get('ujin1')[0].lower().capitalize() if not(dicta.get('ujin1', None) is None) else None #dicta.get('ujin1')[0].lower().capitalize()
            data['ujin2'] = dicta.get('ujin2')[0].lower().capitalize() if not(dicta.get('ujin2', None) is None) else None #dicta.get('ujin2')[0].lower().capitalize()
            data['obedk'] = dicta.get('obedk')[0].lower().capitalize() if not(dicta.get('obedk', None) is None) else None #dicta.get('obedk')[0].lower().capitalize()
            data['obedkg1'] = dicta.get('obedkg1')[0].lower().capitalize() if not(dicta.get('obedkg1', None) is None) else None #dicta.get('obedkg1')[0].lower().capitalize()
            data['obedkg2'] = dicta.get('obedkg2')[0].lower().capitalize() if not(dicta.get('obedkg2', None) is None) else None #dicta.get('obedkg2')[0].lower().capitalize()
            data['obedkg3'] = dicta.get('obedkg3')[0].lower().capitalize() if not(dicta.get('obedkg3', None) is None) else None #dicta.get('obedkg2')[0].lower().capitalize()
            data['internatp'] = dicta.get('internatp')[0].lower().capitalize() if not(dicta.get('internatp', None) is None) else None #dicta.get('obedkg2')[0].lower().capitalize()
            data['zavtrakg'] = dicta.get('zavtrakg')[0].lower().capitalize() if not(dicta.get('zavtrakg', None) is None) else None #dicta.get('obedkg2')[0].lower().capitalize()
            #stolovayainfopit.objects.filter(datapit=data['datpit'], uchid_id=data['uchid']).delete()
            stolovayainfopitafter(datapit=data['datpit'], uchid_id=data['uchid'], zavtrak=data['zavtrak'], obed=data['obed'], poldnik=data['poldnik'], ujin1=data['ujin1'], ujin2=data['ujin2'], obedk=data['obedk'], obedkg1=data['obedkg1'], obedkg2=data['obedkg2'], obedkg3=data['obedkg3'], zavtrakg=data['zavtrakg'], internatp=data['internatp'], datapittime=datetime.now() ).save()
            data['success'] = 'ok'
    context = {'data':data}
    return JsonResponse(data)

@login_required
def AdminReport(request): #Обработчк Репортов!
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin', 'stol-report']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    alertmsg=''
    datamodel0={}
    otchettype=1
    dateminmax = [0,1]
    dateminmax[0]=(datetime.now() + timedelta(days=-365)).strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d")
    datasek = (datetime.now()+timedelta(days=-1)).strftime("%Y-%m-%d")
    datnumofweek = datetime.strptime(datasek,'%Y-%m-%d').weekday()
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
            else:
                datasek = (datetime.now()+timedelta(days=-1)).strftime("%Y-%m-%d")
        if dicta.get('formr1',0) !=0: #VIEWrep1
            del dicta['formr1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
        if dicta.get('otchettype',0) != 0:
            if dicta.get('otchettype')[0] in ['1','2','3']:
                otchettype=int(dicta.get('otchettype')[0])
            else:
                otchettype=1
        else:
            otchettype=1
    if otchettype==1:#ОТЧЕТ№1 СОБЕРЕМ БАЗУ ДЛЯ ЭКСПОРТА ПО ДЕТЯМ С ЛЬГОТАМИ
        queryset = modelstol.objects.all().order_by('classname','fio')
        #1
        lgotaarrlist = get_typesofeda()
        list_of_unique_eda = {}#[]
        unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))
        for eda in unique_eda:
            list_of_unique_eda.update({eda:0})
        lgotaarr = list_of_unique_eda
        #1
        datamodel1 = []
        sumuch = 0

#        datamodelas = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
        queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
        stolcat = set(stolovayacategory.objects.all())
#        stolmed = set(stolovayamedflag.objects.all())
#        modeldatapit=set(stolovayainfopit.objects.all().order_by('-datapittime'))
        for stolm in queryset :
            stolm.typeofeda = 'normal'
            stolm = stolcategoryget(stolm, datasek, stolcat)
#            stolm.medflag = False
#            stolm = stolmedflagget(stolm, datasek, stolmed)


#            stolm.eda = {'zavtrak':0,'obed':0,'poldnik':0, 'ujin1':0, 'ujin2':0, 'obedk':0, 'obedkg1':0, 'obedkg2':0}
#            stolm.eda.update(func_read_int(stolm.id, datasek, stolm.typeofeda, modeldatapit=modeldatapit))

            stolm.chkflag = False
#            stolm = stolchkflagget(stolm, datasek, datamodel)

            sumuch += 1
            datamodel1.append(stolm)

    if otchettype==2:#ОТЧЕТ№2 СОБЕРЕМ БАЗУ ДЛЯ ЭКСПОРТА ПО ДЕТЯМ С ЛЬГОТАМИ и питанием
        dateminmaxrep = [0,1]
        dateminmaxrep[0]=(datetime.now() + timedelta(days=-3)).strftime("%Y-%m-%d")
        dateminmaxrep[1]=(datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d")
        queryset = modelstol.objects.all()
        #1
        lgotaarrlist = get_typesofeda()
        list_of_unique_eda = {}#[]
        unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))
        for eda in unique_eda:
            list_of_unique_eda.update({eda:0})
        lgotaarr = list_of_unique_eda
        #1
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            if dicta.get('form2',0) !=0: #VIEWHIST
                del dicta['form2']
                del dicta['csrfmiddlewaretoken']
                if dicta.get('datepickerre', 0) != 0 or dicta.get('datepickerre', 0) != '':
                    dateminmaxrep[1] = dicta.get('datepickerre')[0]
                    del dicta['datepickerre']
                if dicta.get('datepickerrs', 0) != 0 or dicta.get('datepickerrs', 0) != '':
                    dateminmaxrep[0] = dicta.get('datepickerrs')[0]
                    del dicta['datepickerrs']

        datamodel1 = []
        sumuch = 0
        datamodelas1 = stolovayainfodata.objects.filter(Q(datapit__gte=dateminmaxrep[0]),Q(datapit__lte=dateminmaxrep[1])).order_by('-datazapis')
        delta1day = timedelta(days=1)
        datasek1 = datetime.strptime(dateminmaxrep[0],'%Y-%m-%d').date() - delta1day
        dataiter = 0
        datarepout = '='
        lgotaarr = mlgotaarrvseda.copy()
        eda2 = mlgotaarrvseda.copy()
        queryset = modelstol.objects.filter(pitendateen__lte=dateminmaxrep[1], pitendatedi__gte=dateminmaxrep[0])
        stolcat = set(stolovayacategory.objects.all())
        stolmed = set(stolovayamedflag.objects.all())
        stoldiet = set(stolovayadietflag.objects.all())
        modeldatapit1=stolovayainfopit.objects.filter(Q(datapit__gte=dateminmaxrep[0]),Q(datapit__lte=dateminmaxrep[1])).order_by('-datapittime')
        modeldatapitaf1=stolovayainfopitafter.objects.filter(Q(datapit__gte=dateminmaxrep[0]),Q(datapit__lte=dateminmaxrep[1])).order_by('-datapittime')
#        chekflagtxt = {}
#        chekflagtxt[9] = ''
        tmpsumeda = {}
        while (datasek1 < datetime.strptime(dateminmaxrep[1],'%Y-%m-%d').date()):
            datasek1 += delta1day
            datasek2 = datetime.strftime(datasek1,'%Y-%m-%d')
            datnumofweek = datetime.strptime(datasek2,'%Y-%m-%d').weekday()
            dataiter += 1
            datamodelas = datamodelas1.filter(datapit=datasek2)
            modeldatapit = modeldatapit1.filter(datapit=datasek2)
            modeldatapitaf = modeldatapitaf1.filter(datapit=datasek2)
            for stolm in queryset :
                if not ((datasek1 >= stolm.pitendateen) and (datasek1 <= stolm.pitendatedi)):
                    if dataiter == 1:
                        stolm.eda2 = mlgotaarrvseda.copy()
                        stolm.a = ''
                        tmpsumeda[stolm.id] = 0
                    continue
                stolm.chkflag = False
                stolm = stolchkflagget(stolm, datasek2, datamodelas)
                stolm.eda = mlgotaarrvseda.copy()
                stolm.eda3 = mlgotaarrvseda.copy()
                if dataiter == 1:
                    stolm.eda2 = mlgotaarrvseda.copy()
                    stolm.a = ''
                    tmpsumeda[stolm.id] = 0
                if ((stolm.chkflag == True) or (stolm.chkflag == 'True')):
                    continue
#                if ((stolm.classname == '1XKO') and (datnumofweek == 2)):
#                    continue

                stolm.typeofeda = 'normal'
                stolm = stolcategoryget(stolm, datasek2, stolcat)
                if stolm.typeofeda in ['normal','internat14','internat59','lgota14','lgota59']:
                    if dataiter == 1:
                        stolm.eda2 = mlgotaarrvseda.copy()
                        stolm.a = ''
                        tmpsumeda[stolm.id] = 0
                    continue
                stolm.medflag = False
                stolm = stolmedflagget(stolm, datasek2, stolmed)

                stolm.dietflag = False
                stolm = stoldietflagget(stolm, datasek2, stoldiet)

                if ((stolm.chkflag == False) or (stolm.chkflag == "False")) :
                    if not hasattr(stolm, 'datazapis'):
                        if not((stolm.typeofeda == 'internat14') or (stolm.typeofeda == 'internat59') or (stolm.typeofeda == 'internatp')):
                             if (datnumofweek == 6):
                                continue
                        ##################KOSTIL################################
#                        if ((stolm.classname == '103A') and (stolm.typeofeda != 'internat14') and (datnumofweek == 5)):
#                            continue
                        ##################KOSTIL################################
                    stolm.eda.update(func_read_int(stolm.id, datasek2, stolm.typeofeda, modeldatapit=modeldatapit))
                    stolm.eda3.update(func_read_int_fact(stolm.id, datasek2, stolm.typeofeda, modeldatapit=modeldatapitaf))
                    if 'datapittime' in stolm.eda3:
                         stolm.eda = stolm.eda3

                    if stolm.eda['zavtrak'] == True or stolm.eda['zavtrak'] == 'True':
                        stolm.eda2['zavtrak'] += 1
                        eda2['zavtrak'] += 1
                    if stolm.eda['obed'] == True or stolm.eda['obed'] == 'True':
                        stolm.eda2['obed'] += 1
                        eda2['obed'] += 1
                    if stolm.eda['poldnik'] == True or stolm.eda['poldnik'] == 'True':
                        stolm.eda2['poldnik'] += 1
                        eda2['poldnik'] += 1
                    if stolm.eda['ujin1'] == True or stolm.eda['ujin1'] == 'True':
                        stolm.eda2['ujin1'] += 1
                        eda2['ujin1'] += 1
                    if stolm.eda['ujin2'] == True or stolm.eda['ujin2'] == 'True':
                        stolm.eda2['ujin2'] += 1
                        eda2['ujin2'] += 1
                    if stolm.eda['obedk'] == True or stolm.eda['obedk'] == 'True':
                        stolm.eda2['obedk'] += 1
                        eda2['obedk'] += 1
                    if stolm.eda['obedkg1'] == True or stolm.eda['obedkg1'] == 'True':
                        stolm.eda2['obedkg1'] += int(stolm.xvarx)
                        eda2['obedkg1'] += int(stolm.xvarx)
                    if stolm.eda['obedkg2'] == True or stolm.eda['obedkg2'] == 'True':
                        stolm.eda2['obedkg2'] += int(stolm.xvarx)
                        eda2['obedkg2'] += int(stolm.xvarx)
                    if stolm.eda['obedkg3'] == True or stolm.eda['obedkg3'] == 'True':
                        stolm.eda2['obedkg3'] += int(stolm.xvarx)
                        eda2['obedkg3'] += int(stolm.xvarx)
                    if stolm.eda['internatp'] == True or stolm.eda['internatp'] == 'True':
                        stolm.eda2['internatp'] += int(stolm.xvarx)
                        eda2['internatp'] += int(stolm.xvarx)
                    if stolm.eda['zavtrakg'] == True or stolm.eda['zavtrakg'] == 'True':
                        stolm.eda2['zavtrakg'] += 1
                        eda2['zavtrakg'] += 1
                    if (sum(stolm.eda2.values())>=1) :
                        if ('datpit' in stolm.eda):
                            if (sum(stolm.eda2.values()) > tmpsumeda[stolm.id]):
                                tmpsumeda[stolm.id] = sum(stolm.eda2.values())
                                stolm.a +=  str(datasek2) + ', '#str(stolm.eda['datpit']) + ', '#+ str(resofchk.__dict__) + ', '
#               nachalkaclass = ['103A','103B','104A','104B']
#                if stolm.typeofeda == 'normal':
#                    if not(stolm.classname in nachalkaclass):
#                        stolm.eda.pop('zavtrak')
#                    stolm.eda.pop('obed')
#                    stolm.eda.pop('poldnik')
#                    stolm.eda.pop('ujin1')
#                    stolm.eda.pop('ujin2')
#                    stolm.eda.pop('obedk')
#                if stolm.typeofeda == 'lgota14':
#                    stolm.eda.pop('obed')
#                    stolm.eda.pop('poldnik')
#                    stolm.eda.pop('ujin1')
#                    stolm.eda.pop('ujin2')
#                if stolm.typeofeda == 'lgota59':
#                    stolm.eda.pop('zavtrak')
#                    stolm.eda.pop('obed')
#                    stolm.eda.pop('poldnik')
#                    stolm.eda.pop('ujin1')
#                    stolm.eda.pop('ujin2')
#                if ((stolm.typeofeda == 'internat14') or (stolm.typeofeda == 'internat59')):
#                    stolm.eda.pop('obedk')


                if list(set(filter(lambda x: x.id == stolm.id , datamodel1))) == []:
                    datamodel1.append(stolm)
                    sumuch += 1

    if otchettype==3:#ОТЧЕТ№3 СОБЕРЕМ по дням для бухгалтерии
        dateminmaxrep = [0,1]
        dateminmaxrep[0]=(datetime.now() + timedelta(days=-3)).strftime("%Y-%m-%d")
        dateminmaxrep[1]=(datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d")
        queryset = modelstol.objects.all()
        #1
        lgotaarrlist = get_typesofeda()
        list_of_unique_eda = {}#[]
        unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))
        for eda in unique_eda:
            list_of_unique_eda.update({eda:0})
        lgotaarrvseda = list_of_unique_eda
        #1
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            if dicta.get('form7',0) !=0: #VIEWHIST
                del dicta['form7']
                del dicta['csrfmiddlewaretoken']
                if dicta.get('datepickerre', 0) != 0 or dicta.get('datepickerre', 0) != '':
                    dateminmaxrep[1] = dicta.get('datepickerre')[0]
                    del dicta['datepickerre']
                if dicta.get('datepickerrs', 0) != 0 or dicta.get('datepickerrs', 0) != '':
                    dateminmaxrep[0] = dicta.get('datepickerrs')[0]
                    del dicta['datepickerrs']

        datamodel1 = []
        sumuch = 0
        datamodelas1 = stolovayainfodata.objects.filter(Q(datapit__gte=dateminmaxrep[0]),Q(datapit__lte=dateminmaxrep[1])).order_by('-datazapis')
        delta1day = timedelta(days=1)
        datasek1 = datetime.strptime(dateminmaxrep[0],'%Y-%m-%d').date() - delta1day
        datasek12 = datasek1
        dataiter = 0
        datarepout = '='
        lgotaarr = mlgotaarrvseda.copy()
        eda2 = mlgotaarrvseda.copy()
        unique_day=[]
        stolpodacha = stolovayapodacha.objects.filter(site=Site.objects.get_current())[:1].get()
        while (datasek12 < datetime.strptime(dateminmaxrep[1],'%Y-%m-%d').date()):
            datasek12 += delta1day
            datasek22 = datetime.strftime(datasek12,'%Y-%m-%d')
            unique_day.append(datasek22)

        list_of_unique_eda_day_eda = {}
        list_of_unique_eda_day_eda14 = {}
        for day42 in unique_day:
            list_of_unique_eda_day_eda[day42] = {}
            list_of_unique_eda_day_eda14[day42] = {}
            for eda in lgotaarr:
                list_of_unique_eda_day_eda[day42].update({eda:0})
                list_of_unique_eda_day_eda14[day42].update({eda:0})

        queryset = modelstol.objects.filter(pitendateen__lte=dateminmaxrep[1], pitendatedi__gte=dateminmaxrep[0])
        stolcat = set(stolovayacategory.objects.all())
        stolmed = set(stolovayamedflag.objects.all())
        stoldiet = set(stolovayadietflag.objects.all())
        modeldatapit1=stolovayainfopit.objects.filter(Q(datapit__gte=dateminmaxrep[0]),Q(datapit__lte=dateminmaxrep[1])).order_by('-datapittime')
        modeldatapitaf1=stolovayainfopitafter.objects.filter(Q(datapit__gte=dateminmaxrep[0]),Q(datapit__lte=dateminmaxrep[1])).order_by('-datapittime')
        tmpsumeda = {}
        #enditer=0
        resultikas = ""
        #resultikas += str(queryset.count())
        #stolmobj = {}
        nachclass = mnachalkaclass.keys()#['103A','104A','104B', '104V']
        while (datasek1 < datetime.strptime(dateminmaxrep[1],'%Y-%m-%d').date()):
            #del(stolmobj)
            #stolmobj = {}
            datasek1 += delta1day
            datasek2 = datetime.strftime(datasek1,'%Y-%m-%d')
            datnumofweek = datetime.strptime(datasek2,'%Y-%m-%d').weekday()
            dataiter += 1
            #datarepout = datarepout + str(datasek1) + '-' + str(datasek2) + '_/_'
            #queryset = filter(lambda x:((x.pitendateen<=datasek1) and (x.pitendatedi>=datasek1)), queryset1)
            datamodelas = datamodelas1.filter(datapit=datasek2)
            modeldatapit = modeldatapit1.filter(datapit=datasek2)
            modeldatapitaf = modeldatapitaf1.filter(datapit=datasek2)
            #stolm={}
            for stolm in queryset :
                #enditer+=1
                stolm.eda = mlgotaarrvseda.copy()
                stolm.eda3 = mlgotaarrvseda.copy()
                if dataiter == 1:
                    stolm.eda2 = mlgotaarrvseda.copy()
                    stolm.a = ''
                    tmpsumeda[stolm.id] = 0
                if not ((datasek1 >= stolm.pitendateen) and (datasek1 <= stolm.pitendatedi)):
                    continue
#                if ((stolm.classname == '1XKO') and (datnumofweek == 2)):
#                    continue
                stolm.chkflag = False
                stolm = stolchkflagget(stolm, datasek2, datamodelas)

                if ((stolm.chkflag == True) or (stolm.chkflag == 'True')):
                    continue

                stolm.typeofeda = 'normal'
                stolm = stolcategoryget(stolm, datasek2, stolcat)

                stolm.medflag = False
                stolm = stolmedflagget(stolm, datasek2, stolmed)

                stolm.dietflag = False
                stolm = stoldietflagget(stolm, datasek2, stoldiet)

                #resofchk = stolchkflagget(stolm, datasek2, datamodelas)

                #stolm.eda2['datspit'] += str(stolm.chkflag)

                if ((stolm.chkflag == False) or (stolm.chkflag == "False")) :
#                    if hasattr(stolm, 'datazapis'):
#                        if not ((stolm.classname == '1XKO') and (datnumofweek == 2)):
#                            if not(not((stolm.typeofeda == 'internat14') or (stolm.typeofeda == 'internat59')) and (datnumofweek == 6)):
##                                stolm.eda.update(func_read_int(stolm.id, datasek2, stolm.typeofeda, modeldatapit=modeldatapit))
#                                stolm.eda.update(func_read(stolm.id, datasek2, stolm.typeofeda, medflag=stolm.medflag, timestolmodel=stolpodacha, modeldatapit=modeldatapit))
##                                stolm.eda3.update(func_read_int_fact(stolm.id, datasek2, stolm.typeofeda, modeldatapit=modeldatapitaf))
##                    if 'datapittime' in stolm.eda3:
##                        stolm.eda = stolm.eda3
#                    stolm.a += str(datasek2) + ' step0 '
                    if not (hasattr(stolm, 'datazapis') or hasattr(stolm, 'chkflgd')):
#                        stolm.a += ' step1 '
                        if not(stolm.typeofeda in ['internat14', 'internat59', 'internatp']):
#                            stolm.a += ' step2 '
                            if (datnumofweek == 6):
#                                stolm.a += ' step3 '
                                continue
                        ##################KOSTIL################################
#                        if ((stolm.classname == '103A') and (stolm.typeofeda != 'internat14') and (datnumofweek == 5)):
#                            continue
                        ##################KOSTIL################################
                    stolm.eda.update(func_read_int(stolm.id, datasek2, stolm.typeofeda, modeldatapit=modeldatapit))
                    stolm.eda3.update(func_read_int_fact(stolm.id, datasek2, stolm.typeofeda, modeldatapit=modeldatapitaf))
                    if 'datapittime' in stolm.eda3:
                        stolm.eda = stolm.eda3
                    if stolm.eda['zavtrak'] == True or stolm.eda['zavtrak'] == 'True':
                        stolm.eda2['zavtrak'] += 1
                        list_of_unique_eda_day_eda[datasek2]['zavtrak'] += 1
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['zavtrak'] += 1
                    if stolm.eda['obed'] == True or stolm.eda['obed'] == 'True':
                        stolm.eda2['obed'] += 1
                        list_of_unique_eda_day_eda[datasek2]['obed'] += 1
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['obed'] += 1
                    if stolm.eda['poldnik'] == True or stolm.eda['poldnik'] == 'True':
                        stolm.eda2['poldnik'] += 1
                        list_of_unique_eda_day_eda[datasek2]['poldnik'] += 1
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['poldnik'] += 1
                    if stolm.eda['ujin1'] == True or stolm.eda['ujin1'] == 'True':
                        stolm.eda2['ujin1'] += 1
                        list_of_unique_eda_day_eda[datasek2]['ujin1'] += 1
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['ujin1'] += 1
                    if stolm.eda['ujin2'] == True or stolm.eda['ujin2'] == 'True':
                        stolm.eda2['ujin2'] += 1
                        list_of_unique_eda_day_eda[datasek2]['ujin2'] += 1
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['ujin2'] += 1
                    if stolm.eda['obedk'] == True or stolm.eda['obedk'] == 'True':
                        stolm.eda2['obedk'] += 1
                        list_of_unique_eda_day_eda[datasek2]['obedk'] += 1
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['obedk'] += 1
                    if stolm.eda['obedkg1'] == True or stolm.eda['obedkg1'] == 'True':
                        stolm.eda2['obedkg1'] += 1
                        list_of_unique_eda_day_eda[datasek2]['obedkg1'] += int(stolm.xvarx)
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['obedkg1'] += int(stolm.xvarx)
                    if stolm.eda['obedkg2'] == True or stolm.eda['obedkg2'] == 'True':
                        stolm.eda2['obedkg2'] += 1
                        list_of_unique_eda_day_eda[datasek2]['obedkg2'] += int(stolm.xvarx)
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['obedkg2'] += int(stolm.xvarx)
                    if stolm.eda['obedkg3'] == True or stolm.eda['obedkg3'] == 'True':
                        stolm.eda2['obedkg3'] += 1
                        list_of_unique_eda_day_eda[datasek2]['obedkg3'] += int(stolm.xvarx)
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['obedkg3'] += int(stolm.xvarx)

                    if stolm.eda['internatp'] == True or stolm.eda['internatp'] == 'True':
                        stolm.eda2['internatp'] += 1
                        list_of_unique_eda_day_eda[datasek2]['internatp'] += int(stolm.xvarx)
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['internatp'] += int(stolm.xvarx)


                    if stolm.eda['zavtrakg'] == True or stolm.eda['zavtrakg'] == 'True':
                        stolm.eda2['zavtrakg'] += 1
                        list_of_unique_eda_day_eda[datasek2]['zavtrakg'] += 1
                        if stolm.classname in nachclass:
                            list_of_unique_eda_day_eda14[datasek2]['zavtrakg'] += 1
                    if (sum(stolm.eda2.values())>=1) :
                        if ('datpit' in stolm.eda):
                            if (sum(stolm.eda2.values()) > tmpsumeda[stolm.id]):
                                tmpsumeda[stolm.id] = sum(stolm.eda2.values())
#                                stolm.a +=  str(datasek2) + ', ' + str(datnumofweek) #str(stolm.eda['datpit']) + ', '#+ str(resofchk.__dict__) + ', '

                #datamodel1.append([ datasek2,copy.copy(stolm) ]) ##OK##

#                del(stolm.datapit)
                        #if stolm.id == 191 :
                        #    resultikas = resultikas + ",=," + str(stolm.__dict__)
#                if list(set(filter(lambda x: x.id == stolm.id , datamodel1))) == []:
#                    datamodel1.append(stolm)
#                    sumuch += 1




    #ВЫВОДВЫВОД
    if otchettype==1:
        datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda','classname','fio'))
        context = {'queryset':queryset, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0, 'sumuch':sumuch, 'unique_eda':unique_eda}
        return render(request, 'stolovaya/report.html', context)
    elif otchettype==2:
        datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda','classname','fio'))
        context = {'queryset':queryset, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0, 'sumuch':sumuch, 'unique_eda':unique_eda, 'dateminmaxrep':dateminmaxrep, 'eda2':eda2}
        return render(request, 'stolovaya/report-uch.html', context)
    elif otchettype==3:
        datamodel0 = list_of_unique_eda_day_eda
        datamodel14 = list_of_unique_eda_day_eda14
        tableofeda = datamodel1
        context = {'queryset':queryset, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datamodel1':datamodel0,'datamodel14':datamodel14, 'sumuch':sumuch, 'unique_eda':unique_eda, 'dateminmaxrep':dateminmaxrep, 'tableofeda':tableofeda, 'resultikas':resultikas }
        return render(request, 'stolovaya/report-uch-v2.html', context)

def stolcategoryget(stolm, datasek2, stolcat):
    tmpfdatpit = datetime.strptime(datasek2,'%Y-%m-%d').date()
    tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
    for objcat in filter(lambda x:x.uchid_id==stolm.id,stolcat):#stolovayacategory.objects.filter(uchid_id=stolm.id):
        if objcat.dateeda >= tmpdatpit:
            if tmpfdatpit >= objcat.dateeda :
                if objcat.datetime1.timestamp() >= tmpfdatpittime.timestamp():
                    tmpdatpit = objcat.dateeda
                    tmpfdatpittime = objcat.datetime1
                    stolm.typeofeda = objcat.category
                    stolm.xvarx = objcat.xvarx
    return stolm

def stolmedflagget(stolm, datasek2, stolmed):
    tmpfdatpit = datetime.strptime(datasek2,'%Y-%m-%d').date()
    tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
    for objcat in filter(lambda x:x.uchid_id==stolm.id,stolmed):#stolovayacategory.objects.filter(uchid_id=stolm.id):
        if objcat.dateeda >= tmpdatpit:
            if tmpfdatpit >= objcat.dateeda :
                if objcat.datetime1.timestamp() >= tmpfdatpittime.timestamp():
                    tmpdatpit = objcat.dateeda
                    tmpfdatpittime = objcat.datetime1
                    stolm.medflag = objcat.medflag
    return stolm

def stoldietflagget(stolm, datasek2, stoldiet):
    tmpfdatpit = datetime.strptime(datasek2,'%Y-%m-%d').date()
    tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
    for objcat in filter(lambda x:x.uchid_id==stolm.id,stoldiet):#stolovayacategory.objects.filter(uchid_id=stolm.id):
        if objcat.dateeda >= tmpdatpit:
            if tmpfdatpit >= objcat.dateeda :
                if objcat.datetime1.timestamp() >= tmpfdatpittime.timestamp():
                    tmpdatpit = objcat.dateeda
                    tmpfdatpittime = objcat.datetime1
                    stolm.dietflag = objcat.dietflag
    return stolm

def stolchkflagget(stolm, datasek2, datamodelas):
    tmpfdatpit = datetime.strptime(datasek2,'%Y-%m-%d').date()
    tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
    #stolm.hkdata=str(datamodelas.__dict__)
    if hasattr(stolm, 'datapit'):
        delattr(stolm, 'datapit')
    if hasattr(stolm, 'datazapis'):
        delattr(stolm, 'datazapis')
    if hasattr(stolm, 'chkflgd'):
        delattr(stolm, 'chkflgd')
    for datm in filter(lambda x:((x.uchid_id==stolm.id) and (str(x.datapit)==datasek2)), datamodelas):#datamodel : #отмеченные дети
        if datm.datazapis.timestamp() >= tmpfdatpittime.timestamp():
            tmpfdatpittime = datm.datazapis
            stolm.chkflag = datm.chkflag
            stolm.datazapis = datm.datazapis
            stolm.datapit = datm.datapit
            stolm.chkflgd = datm.datapit
    return stolm

def stolchkblock(stolm, datasek2, datamodelbl):
    tmpfdatpit = datetime.strptime(datasek2,'%Y-%m-%d').date()
    tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
    tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
    for objcat in filter(lambda x:x.uchid_id==stolm.id,datamodelbl):#stolovayacategory.objects.filter(uchid_id=stolm.id):
        if objcat.dateeda >= tmpdatpit:
            if tmpfdatpit >= objcat.dateeda :
                if objcat.datetime1.timestamp() >= tmpfdatpittime.timestamp():
                    tmpdatpit = objcat.dateeda
                    tmpfdatpittime = objcat.datetime1
                    stolm.blockflag = objcat.blockflag
    return stolm


@login_required
def Scanviewer(request): #Сканер
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin', 'stol-scan']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
        datamodel1 = []
        sumuch = 0
        datasek = (datetime.now()).strftime("%Y-%m-%d")
        datamodelas = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
        queryset = modelstol.objects.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek).order_by('classname','fio')
        stolcat = set(stolovayacategory.objects.all())
        stolmed = set(stolovayamedflag.objects.all())
        stoldiet = set(stolovayadietflag.objects.all())
        modeldatapit=set(stolovayainfopit.objects.filter(datapit=datasek).order_by('-datapittime'))
        querysetmodel1 = stolovayafactstol.objects.filter(dateeda=datetime.now().date()).order_by('-datetime')
        stolfact = stolovayafactstol.objects.filter(dateeda=datasek)
        querysetmodel = []
        edanow = gettimeofeda()
        for stolm in queryset :
            stolm.typeofeda = 'normal'
            stolm = stolcategoryget(stolm, datasek, stolcat)

            stolm.medflag = False
            stolm = stolmedflagget(stolm, datasek, stolmed)
            
            stolm.chkflag = False
            stolm = stolchkflagget(stolm, datasek, datamodelas)
            
            stolm.dietflag = False
            stolm = stoldietflagget(stolm, datasek, stoldiet)
            
            stolm.eda = mlgotaarrvseda.copy()
            stolm.eda0 = medaqr.copy()
            if stolm.chkflag == False: 
                stolm.eda.update(func_read_int(stolm.id, datasek, stolm.typeofeda, modeldatapit=modeldatapit))
                stolm.eda0.update(getlastscantime(stolm.id, datasek, stolm.eda0, stolfact))

            

            sumuch += 1
            datamodel1.append(stolm)

            

            for obj in filter(lambda x: x.uchid_id==stolm.id, querysetmodel1):
                obj.fio =  stolm.fio
                obj.dietflag = stolm.dietflag
                obj.classname = stolm.classname
                querysetmodel.append(obj)

    querysetmodel = sorted(querysetmodel, key=attrgetter('datetime'), reverse=True)
    context = {'datamodel1':datamodel1, 'sumuch':sumuch, 'edanow':edanow, 'datamodel1chk':querysetmodel}
    return render(request, 'stolovaya/qr-code.html', context)

def getlastscantime(stolmid, datasek, eda0, stolfact):
    querysetmodel = filter(lambda x:x.uchid_id==stolmid,stolfact)#stolovayafactstol.objects.filter(dateeda=datasek, uchid_id=stolmid)
#    if querysetmodel.count() > 0:
    if len(list(querysetmodel)) > 0:
        for qmodl in querysetmodel:
            if qmodl.typeofedapit == 'zavtrak':
                eda0['zavtrak'] = qmodl.datetime.strftime("%H:%M:%S")
            if qmodl.typeofedapit == 'zavtrak2':
                eda0['zavtrak2'] = qmodl.datetime.strftime("%H:%M:%S")
            if qmodl.typeofedapit == 'obed':
                eda0['obed'] = qmodl.datetime.strftime("%H:%M:%S")
            if qmodl.typeofedapit == 'poldnik':
                eda0['poldnik'] = qmodl.datetime.strftime("%H:%M:%S")
            if qmodl.typeofedapit == 'ujin1':
                eda0['ujin1'] = qmodl.datetime.strftime("%H:%M:%S")
            if qmodl.typeofedapit == 'ujin2':
                eda0['ujin2'] = qmodl.datetime.strftime("%H:%M:%S")
    return eda0



def gettimeofeda():
    edanow='zavtrak'
    if datetime.now().time() < datetime.strptime('09.10','%H.%M').time():
        edanow='zavtrak'
    if datetime.now().time() > datetime.strptime('10.30','%H.%M').time() and datetime.now().time() < datetime.strptime('12.00','%H.%M').time():
        edanow='zavtrak2'
    if datetime.now().time() > datetime.strptime('12.00','%H.%M').time() and datetime.now().time() < datetime.strptime('16.00','%H.%M').time():
        edanow='obed'
    if datetime.now().time() > datetime.strptime('16.00','%H.%M').time() and datetime.now().time() < datetime.strptime('17.30','%H.%M').time():
        edanow='poldnik'
    if datetime.now().time() > datetime.strptime('17.30','%H.%M').time() and datetime.now().time() < datetime.strptime('22.30','%H.%M').time():
        edanow='ujin1'
    if datetime.now().time() > datetime.strptime('20.10','%H.%M').time() and datetime.now().time() < datetime.strptime('21.00','%H.%M').time():
        edanow='ujin2'
    return edanow

#from silk.profiling.profiler import silk_profile
#@silk_profile(name='ScanScan')

@login_required
def scanscan(request, *args, **kwargs): #Обработчк от сканера
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin','stol-scan']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    data = {}
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            data['uchid'] = dicta.get('uchid')[0]
            data['catofeda'] = dicta.get('catofeda')[0]
            querysetmodel = stolovayafactstol.objects.filter(dateeda=datetime.now().date(), uchid_id=data['uchid'], typeofedapit=data['catofeda']).values_list('id')
            #if data['catofeda'] == 'zavtrak':
            #list(filter(lambda x:x.typeofedapit==data['catofeda'],querysetmodel))
            if len(list(querysetmodel)) < 1:
                stolovayafactstol(datetime=datetime.now(), dateeda=datetime.now().date(), typeofedapit=data['catofeda'], uchid_id=data['uchid']).save()
                data['valid'] = 'ОК'
            else:
                data['valid'] = 'Повтор'
            data['last'] = datetime.now()
            data['success'] = 'ok'
#    context = {'data':data}
    return JsonResponse(data)


@login_required
def qrcodeview(request): #Просмотр QR-кодов
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin', 'stol-scan', 'stol-view']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
        #import qrcode
        #from io import BytesIO
        #import qrcode.image.svg
        #import base64
        lgotaarrlist = get_typesofeda()
        list_of_unique_eda = {}#[]
        list_of_unique_eda_class = {}#[]
        unique_eda =sorted(set( dic for dic,dic2 in lgotaarrlist ),key=len, reverse=True)
        selitcat = "allstar"
        datasek = (datetime.now()).strftime("%Y-%m-%d")
        if request.method == 'POST' and request.POST:
            dicta = dict(request.POST)
            if dicta.get('form1',0) !=0:
                del dicta['form1']
                del dicta['csrfmiddlewaretoken']
                if dicta.get('selitcat',0) !=0:
                    selitcat = dicta.get('selitcat',0)[0]
                if dicta.get('datepicker',0) !=0:
                    datasek = dicta.get('datepicker',0)[0]

        datamodel1 = []
        sumuch = 0
        stolcat = set(stolovayacategory.objects.all())
        stoldiet = set(stolovayadietflag.objects.all())
        queryset = modelstol.objects.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek).order_by('classname','fio')
        #factory = qrcode.image.svg.SvgImage
        nachclass = mnachalkaclass.copy()
        for stolm in queryset :
            stolm.typeofeda = 'normal'
            stolm = stolcategoryget(stolm, datasek, stolcat)
            stolm.dietflag = False
            stolm = stoldietflagget(stolm, datasek, stoldiet)
            if selitcat == "all":
                aok=1
            elif selitcat == "allstar":
                if not(stolm.classname in nachclass):
                    if (stolm.typeofeda in {'normal'}):
                        continue
                else:
                    continue
            elif selitcat == "allnach":
                if (stolm.classname in nachclass):
                    if (stolm.typeofeda in {'normal'}):
                        continue
                else:
                    continue
            else:
                if not(stolm.typeofeda == selitcat):
                    continue
            #img = qrcode.make(str(stolm.id)+'='+str(stolm.qrcode), image_factory=factory, box_size=20)
            #stream = BytesIO()
            #img.save(stream)
            stolm.qrcodeimg = str(stolm.id)+'='+str(stolm.qrcode)#stream.getvalue().decode()
            #stolm.qrcodeimg = 'data:image/svg+xml;utf8;base64,' + base64.b64encode(stream.getvalue()).decode()
            datamodel1.append(stolm)

    context = {'datamodel1':datamodel1, 'unique_eda':unique_eda, 'selitcat':selitcat, 'datasek':datasek}
    return render(request, 'stolovaya/qr-viewer.html', context)

@login_required
def indexpage(request): #mainpage index.html
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin','stol-scan', 'med-ed', 'int-ed', 'class-ed', 'stol-view', 'stol-correct', 'stol-report']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    #конец проверки доступа
    context = {'usergr':unique_groups}
    return render(request, 'stolovaya/index.html', context)



@login_required
def AdminKanikuls(request): #EDIT-Kanikuls
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=120)).strftime("%Y-%m-%d")


    queryset = modelstol.objects.all().order_by('classname','fio')
#    datamodel = stolovayainfodata.objects.all()
    #1
    #lgotaarrlist = queryset.values('typeofeda')
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
#    unique_eda = sorted(set( val for dic in lgotaarrlist for val in dic.values()))
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))

    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1
    if idcl==0:
        return redirect('/login/?next=%s' % request.path)
#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    selit = selectitems2[0]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    datasek2 = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                if ((dicta.get('datepicker')[0] < dateminmax[1]) and (dicta.get('datepicker')[0] > dateminmax[0])):
                    datasek = dicta.get('datepicker')[0]
                else:
                    datasek = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")
            if dicta.get('datepicker2', 0) != 0 or dicta.get('datepicker2', 0) != '':
                if ((dicta.get('datepicker2')[0] < dateminmax[1]) and (dicta.get('datepicker2')[0] > dateminmax[0])):
                    datasek2 = dicta.get('datepicker2')[0]
                else:
                    datasek2 = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker2']
            else:
                datasek2 = datetime.now().strftime("%Y-%m-%d")
            if datasek2 < datasek:
                datasek2=datasek

        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                if ((dicta.get('datepicker')[0] < dateminmax[1]) and (dicta.get('datepicker')[0] > dateminmax[0])):
                    datasek = dicta.get('datepicker')[0]
                else:
                    datasek = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")
            if dicta.get('datepicker2', 0) != 0 or dicta.get('datepicker2', 0) != '':
                if ((dicta.get('datepicker2')[0] < dateminmax[1]) and (dicta.get('datepicker2')[0] > dateminmax[0])):
                    datasek2 = dicta.get('datepicker2')[0]
                else:
                    datasek2 = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker2']
            else:
                datasek2 = datetime.now().strftime("%Y-%m-%d")
            if datasek2 < datasek:
                datasek2=datasek
            datid = ''
            datchk = ''
            tmpmsg = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]
            queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
            for objdi, objdc in arrdata:
                if datetime.now().timestamp()<(datetime.strptime(datasek,'%Y-%m-%d').replace(hour=9, minute=16)).timestamp():
#                    stolovayainfodata.objects.filter(datapit=datdate[0],uchid_id=objdi).delete()
#                    stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                    delta1day = timedelta(days=1)
                    datasek12 = datetime.strptime(datasek,'%Y-%m-%d').date()
                    while (datasek12 <= datetime.strptime(datasek2,'%Y-%m-%d').date()):
                        datasek122 = datetime.strftime(datasek12,'%Y-%m-%d')
                        #objdi ЭТО целевой КЛАСС
                        if objdc == 'True':
                            for stolm in queryset:
                                if stolm.classname == objdi:
                                    stolovayainfodata(datapit=datasek122, uchid_id=stolm.id, chkflag=objdc, datazapis=timezone.now()).save()
                                    tmpmsg += ' ' + str(datasek122) + ' - ' + str(objdi) + '=' + str(objdc)
                        datasek12 += delta1day
                    alertmsg ='Данные ЗАПИСАНЫ Спасибо!'
                else:
                    alertmsg ='Вы пытаетесь ввести данные на сегодняшнюю дату после разрешенного времени(текущая дата 9.15)'
            alertmsg += tmpmsg + str(datasek) + " " + str(datasek2)

    datamodel1 = []
    sumuch = 0
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek, classname=str(selit))
    datamodel = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    for stolm in queryset :

        stolm.medflag = False
        stolm = stolmedflagget(stolm, datasek, stolmed)

        if stolm.medflag == True:
            continue

        if str(selit) == stolm.classname:
            stolm.typeofeda = 'normal'
            stolm = stolcategoryget(stolm, datasek, stolcat)

            stolm.chkflag = False
            stolm = stolchkflagget(stolm, datasek, datamodel)
#            if not (stolm.typeofeda == 'internat14' or stolm.typeofeda == 'internat59'):
            #datamodel1.append(stolm)
#            if 
            sumuch += 1

    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))

    context = {'queryset':queryset1,  'selectitems':selectitems2, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datasek2':datasek2, 'datamodel1':datamodel0, 'sumuch':sumuch}
    return render(request, 'stolovaya/stol-kanikuls.html', context)

@login_required
def AdminKanikuls2(request): #EDIT-Kanikuls2
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=120)).strftime("%Y-%m-%d")


    queryset = modelstol.objects.all().order_by('classname','fio')
#    datamodel = stolovayainfodata.objects.all()
    #1
    #lgotaarrlist = queryset.values('typeofeda')
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
#    unique_eda = sorted(set( val for dic in lgotaarrlist for val in dic.values()))
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))

    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1
    if idcl==0:
        return redirect('/login/?next=%s' % request.path)
#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    selit = selectitems2[0]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    datasek2 = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                if ((dicta.get('datepicker')[0] < dateminmax[1]) and (dicta.get('datepicker')[0] > dateminmax[0])):
                    datasek = dicta.get('datepicker')[0]
                else:
                    datasek = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")
            if dicta.get('datepicker2', 0) != 0 or dicta.get('datepicker2', 0) != '':
                if ((dicta.get('datepicker2')[0] < dateminmax[1]) and (dicta.get('datepicker2')[0] > dateminmax[0])):
                    datasek2 = dicta.get('datepicker2')[0]
                else:
                    datasek2 = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker2']
            else:
                datasek2 = datetime.now().strftime("%Y-%m-%d")
            if datasek2 < datasek:
                datasek2=datasek

        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                if ((dicta.get('datepicker')[0] < dateminmax[1]) and (dicta.get('datepicker')[0] > dateminmax[0])):
                    datasek = dicta.get('datepicker')[0]
                else:
                    datasek = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")
            if dicta.get('datepicker2', 0) != 0 or dicta.get('datepicker2', 0) != '':
                if ((dicta.get('datepicker2')[0] < dateminmax[1]) and (dicta.get('datepicker2')[0] > dateminmax[0])):
                    datasek2 = dicta.get('datepicker2')[0]
                else:
                    datasek2 = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker2']
            else:
                datasek2 = datetime.now().strftime("%Y-%m-%d")
            if datasek2 < datasek:
                datasek2=datasek
            datid = ''
            datchk = ''
            tmpmsg = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]
            queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
            for objdi, objdc in arrdata:
                if datetime.now().timestamp()<(datetime.strptime(datasek,'%Y-%m-%d').replace(hour=9, minute=16)).timestamp():
#                    stolovayainfodata.objects.filter(datapit=datdate[0],uchid_id=objdi).delete()
#                    stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                    delta1day = timedelta(days=1)
                    datasek12 = datetime.strptime(datasek,'%Y-%m-%d').date()
                    while (datasek12 <= datetime.strptime(datasek2,'%Y-%m-%d').date()):
                        datasek122 = datetime.strftime(datasek12,'%Y-%m-%d')
                        #objdi ЭТО целевой КЛАСС
                        if objdc == 'True':
                            #for stolm in queryset:
                                #if stolm.classname == objdi:
                            stolovayainfodata(datapit=datasek122, uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                            tmpmsg += ' ' + str(datasek122) + ' - ' + str(objdi) + '=' + str(objdc)
                        datasek12 += delta1day
                    alertmsg ='Данные ЗАПИСАНЫ Спасибо!'
                else:
                    alertmsg ='Вы пытаетесь ввести данные на сегодняшнюю дату после разрешенного времени(текущая дата 9.15)'
            alertmsg += tmpmsg + str(datasek) + " " + str(datasek2)

    datamodel1 = []
    sumuch = 0
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
    datamodel = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    for stolm in queryset :

#        stolm.medflag = False
#        stolm = stolmedflagget(stolm, datasek, stolmed)
#
#        if stolm.medflag == True:
#            continue

        if str(selit) == stolm.classname:
            stolm.medflag = False
            stolm = stolmedflagget(stolm, datasek, stolmed)
    
            if stolm.medflag == True:
                continue

            stolm.typeofeda = 'normal'
            stolm = stolcategoryget(stolm, datasek, stolcat)

            stolm.chkflag = False
            stolm = stolchkflagget(stolm, datasek, datamodel)
#            if not (stolm.typeofeda == 'internat14' or stolm.typeofeda == 'internat59'):
            datamodel1.append(stolm)
#            if 
            sumuch += 1

    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))

    context = {'queryset':queryset1,  'selectitems':selectitems2, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datasek2':datasek2, 'datamodel1':datamodel0, 'sumuch':sumuch, 'selit':selit}
    return render(request, 'stolovaya/stol-kanikuls2.html', context)




















@login_required
def AdminEndOfYear(request): #EDIT-KonecGoda
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=120)).strftime("%Y-%m-%d")


    queryset = modelstol.objects.all().order_by('classname','fio')
#    datamodel = stolovayainfodata.objects.all()
    #1
    #lgotaarrlist = queryset.values('typeofeda')
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
#    unique_eda = sorted(set( val for dic in lgotaarrlist for val in dic.values()))
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))

    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1
    if idcl==0:
        return redirect('/login/?next=%s' % request.path)
#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    selit = selectitems2[0]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    datasek2 = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                if ((dicta.get('datepicker')[0] < dateminmax[1]) and (dicta.get('datepicker')[0] > dateminmax[0])):
                    datasek = dicta.get('datepicker')[0]
                else:
                    datasek = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")

        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                if ((dicta.get('datepicker')[0] < dateminmax[1]) and (dicta.get('datepicker')[0] > dateminmax[0])):
                    datasek = dicta.get('datepicker')[0]
                else:
                    datasek = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")
            datid = ''
            datchk = ''
            tmpmsg = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]
            queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
            for objdi, objdc in arrdata:
                if datetime.now().timestamp()<(datetime.strptime(datasek,'%Y-%m-%d').replace(hour=23, minute=50)).timestamp():
#                    stolovayainfodata.objects.filter(datapit=datdate[0],uchid_id=objdi).delete()
#                    stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                    delta1day = timedelta(days=1)
                    datasek12 = datetime.strptime(datasek,'%Y-%m-%d').date()
                    #objdi ЭТО целевой КЛАСС
                    if objdc == 'True':
                        for stolm in queryset:
                            if stolm.classname == objdi:
                                #stolovayainfodata(datapit=datasek122, uchid_id=stolm.id, chkflag=objdc, datazapis=timezone.now()).save()
                                modelstol.objects.filter(id=stolm.id).update(pitendatedi=datasek12)
                                tmpmsg += ' ' + str(datasek12) + ' - ' + str(objdi) + '=' + str(objdc)
                    #datasek12 += delta1day
                    alertmsg ='Данные ЗАПИСАНЫ Спасибо!'
                else:
                    alertmsg ='Вы пытаетесь ввести данные на сегодняшнюю дату после разрешенного времени(текущая дата 23.50)'
            alertmsg += tmpmsg + str(datasek) + " " + str(datasek2)

    datamodel1 = []
    sumuch = 0
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek, classname=str(selit))
    datamodel = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    for stolm in queryset :

        stolm.medflag = False
        stolm = stolmedflagget(stolm, datasek, stolmed)

        if stolm.medflag == True:
            continue

        if str(selit) == stolm.classname:
            stolm.typeofeda = 'normal'
            stolm = stolcategoryget(stolm, datasek, stolcat)

            stolm.chkflag = False
            stolm = stolchkflagget(stolm, datasek, datamodel)
#            if not (stolm.typeofeda == 'internat14' or stolm.typeofeda == 'internat59'):
            #datamodel1.append(stolm)
#            if 
            sumuch += 1

    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))

    context = {'queryset':queryset1,  'selectitems':selectitems2, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datasek2':datasek2, 'datamodel1':datamodel0, 'sumuch':sumuch}
    return render(request, 'stolovaya/stol-endofyear.html', context)

@login_required
def AdminEndOfYear2(request): #EDIT-KonecGoda2
    if not request.user.groups.values_list('name',flat = True):
        return redirect('/login/?next=%s' % request.path)
    else:
        flagen=0
        avilgr=['stol-admin']
        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
        for i in avilgr:
            for j in unique_groups:
                if str(i)==str(j):
                    flagen=1
                    break
        if flagen==0 :
            return redirect('/login/?next=%s' % request.path)
    dateminmax = [0,1]
    dateminmax[0]=datetime.now().strftime("%Y-%m-%d")
    dateminmax[1]=(datetime.now() + timedelta(days=120)).strftime("%Y-%m-%d")


    queryset = modelstol.objects.all().order_by('classname','fio')
#    datamodel = stolovayainfodata.objects.all()
    #1
    #lgotaarrlist = queryset.values('typeofeda')
    lgotaarrlist = get_typesofeda()
    list_of_unique_eda = {}#[]
#    unique_eda = sorted(set( val for dic in lgotaarrlist for val in dic.values()))
    unique_eda = sorted(set( dic for dic,dic2 in lgotaarrlist ))

    for eda in unique_eda:
        list_of_unique_eda.update({eda:0})
    lgotaarr = list_of_unique_eda
    #1

    #2
    lgotaarrlist2 = queryset.values('classname')
    list_of_unique_class = {}#[]
    unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
    idcl=0
    for class2 in unique_class:
        if str('stol-admin') in unique_groups:
            list_of_unique_class.update({idcl:class2})#idcl:class2})
            idcl+=1
        else:
            if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1
    if idcl==0:
        return redirect('/login/?next=%s' % request.path)
#    selectitems = unique_class
    selectitems2 = list_of_unique_class
    #2
    selit = selectitems2[0]
    queryset1=[]
    datasek = datetime.now().strftime("%Y-%m-%d")
    datasek2 = datetime.now().strftime("%Y-%m-%d")
    alertmsg=''
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('form2',0) !=0: #VIEWHIST
            del dicta['form2']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                if ((dicta.get('datepicker')[0] < dateminmax[1]) and (dicta.get('datepicker')[0] > dateminmax[0])):
                    datasek = dicta.get('datepicker')[0]
                else:
                    datasek = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")

        if dicta.get('form1',0) !=0: #SAVENEW!!!!
            del dicta['form1']
            del dicta['csrfmiddlewaretoken']
            if dicta.get('selit', 0) != 0:
                selit = dicta.get('selit')[0]
                del dicta['selit']
            if dicta.get('datepicker', 0) != 0 or dicta.get('datepicker', 0) != '':
                if ((dicta.get('datepicker')[0] < dateminmax[1]) and (dicta.get('datepicker')[0] > dateminmax[0])):
                    datasek = dicta.get('datepicker')[0]
                else:
                    datasek = datetime.now().strftime("%Y-%m-%d")
                del dicta['datepicker']
            else:
                datasek = datetime.now().strftime("%Y-%m-%d")
            datid = ''
            datchk = ''
            tmpmsg = ''
            arrdata = []
            for datid, datchk in dicta.items():
                if datid != '':
                    if len(datchk) > 1:
                        arrdata += [(datid[3:],'True')]
                    else:
                        arrdata += [(datid[3:],'False')]
            queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
            for objdi, objdc in arrdata:
                if datetime.now().timestamp()<(datetime.strptime(datasek,'%Y-%m-%d').replace(hour=23, minute=50)).timestamp():
#                    stolovayainfodata.objects.filter(datapit=datdate[0],uchid_id=objdi).delete()
#                    stolovayainfodata(datapit=datdate[0], uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                    delta1day = timedelta(days=1)
                    datasek12 = datetime.strptime(datasek,'%Y-%m-%d').date()
                        #objdi ЭТО целевой КЛАСС
                    if objdc == 'True':
                            #for stolm in queryset:
                                #if stolm.classname == objdi:
                            #stolovayainfodata(datapit=datasek122, uchid_id=objdi, chkflag=objdc, datazapis=timezone.now()).save()
                        modelstol.objects.filter(id=objdi).update(pitendatedi=datasek12)
                        tmpmsg += ' ' + str(datasek12) + ' - ' + str(objdi) + '=' + str(objdc)
#                    datasek12 += delta1day
                    alertmsg ='Данные ЗАПИСАНЫ Спасибо!'
                else:
                    alertmsg ='Вы пытаетесь ввести данные на сегодняшнюю дату после разрешенного времени(текущая дата 23.50)'
            alertmsg += tmpmsg + str(datasek) + " " + str(datasek2)

    datamodel1 = []
    sumuch = 0
    stolcat = set(stolovayacategory.objects.all())
    stolmed = set(stolovayamedflag.objects.all())
    queryset = queryset.filter(pitendateen__lte=datasek, pitendatedi__gte=datasek)
    datamodel = stolovayainfodata.objects.filter(datapit=datasek).order_by('-datazapis')
    for stolm in queryset :

#        stolm.medflag = False
#        stolm = stolmedflagget(stolm, datasek, stolmed)
#
#        if stolm.medflag == True:
#            continue

        if str(selit) == stolm.classname:
            stolm.medflag = False
            stolm = stolmedflagget(stolm, datasek, stolmed)
    
            if stolm.medflag == True:
                continue

            stolm.typeofeda = 'normal'
            stolm = stolcategoryget(stolm, datasek, stolcat)

            stolm.chkflag = False
            stolm = stolchkflagget(stolm, datasek, datamodel)
#            if not (stolm.typeofeda == 'internat14' or stolm.typeofeda == 'internat59'):
            datamodel1.append(stolm)
#            if 
            sumuch += 1

    datamodel0 = sorted(datamodel1, key=attrgetter('typeofeda'))#itemgetter('typeofeda'))

    context = {'queryset':queryset1,  'selectitems':selectitems2, 'alertmsg':alertmsg, 'dateminmax':dateminmax, 'datasek':datasek, 'datasek2':datasek2, 'datamodel1':datamodel0, 'sumuch':sumuch, 'selit':selit}
    return render(request, 'stolovaya/stol-endofyear2.html', context)
