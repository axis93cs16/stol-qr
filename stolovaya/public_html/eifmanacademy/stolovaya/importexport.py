from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, HttpResponse, render
from datetime import datetime, timedelta
from stolovaya.models import stolovaya as modelstol
from stolovaya.models import stolovayainfodata, stolovayainfopit, stolovayapodacha, stolovayatalon, stolovayacategory, get_typesofeda,get_typesofinternat, stolovayapriemipishi, stolovayamedflag, stolovayainfopitafter, stolovayafactstol
import csv
import copy
from collections import defaultdict
import tablib

class RowResult:
    IMPORT_TYPE_UPDATE = 'update'
    IMPORT_TYPE_NEW = 'new'
    IMPORT_TYPE_DELETE = 'delete'
    IMPORT_TYPE_SKIP = 'skip'
    IMPORT_TYPE_ERROR = 'error'
    IMPORT_TYPE_INVALID = 'invalid'

    valid_import_types = frozenset([
        IMPORT_TYPE_NEW,
        IMPORT_TYPE_UPDATE,
        IMPORT_TYPE_DELETE,
        IMPORT_TYPE_SKIP,
    ])

    def __init__(self):
        self.errors = []
        self.validation_error = None
        self.diff = None
        self.import_type = None
        self.row_values = {}
        self.object_id = None
        self.object_repr = None

    def add_instance_info(self, instance):
        if instance is not None:
            # Add object info to RowResult (e.g. for LogEntry)
            self.object_id = getattr(instance, "pk", None)
            self.object_repr = force_str(instance)

@login_required
def getfilecsv(request):
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
    submitok = 0
    datasek = datetime.now().strftime("%Y-%m-%d")
    if request.method == 'POST' and request.POST:
        dicta = dict(request.POST)
        if dicta.get('submitok',0) != 0:
            if dicta.get('submitok',0)[0] == 78 or dicta.get('submitok',0)[0] == "78":
                submitok = 1
                del dicta['submitok']
        if dicta.get('datepicker', 'nothing1') == 'nothing1':
            datasek = datetime.now().strftime("%Y-%m-%d")
        else:
            datasek = dicta.get('datepicker')[0]
            del dicta['datepicker']
    else:
        return redirect('/login/?next=%s' % request.path)
#    file_obj_post = request.POST.get('file')
    file_obj = request.FILES['file']
    csv_reader = csv.DictReader(file_obj.read().decode('utf-8').splitlines(), delimiter=',')
    csv_data = list(row for row in csv_reader) # получиласть модель которую можно разобрать циклом беря данные по ключам и сопоставляя их с моделью
    csv_keys = csv_reader.fieldnames
#    csv_keys = list([row.keys() for row in csv_data][0])
#    csv_keys = csv_data.keys()
    stol_keys =  list([field.name for field in modelstol._meta.fields])
    if set(stol_keys).issubset(csv_keys):
        outtxt = str(csv_keys) + " = " + str(stol_keys) + "OK(main)-Файл готов к импорту!"
    else:
        outtxt = str(csv_keys) + " = " + str(stol_keys) + "FAIL(main)-файл неправильный!"
        return HttpResponse(outtxt) #отсутствуют данные по основной таблице
    stolcat_keys = list([field.name for field in stolovayacategory._meta.fields])
    stolcat_keys.remove('id') #удаляем лишние ключи для проверки
    stolcat_keys.remove('datetime1') #удаляем лишние ключи для проверки
    stolcat_keys.remove('xvarx') #удаляем лишние ключи для проверки
    stolcat_keys.remove('uchid') #удаляем лишние ключи для проверки
    stolcat_keys.remove('dateeda') #удаляем лишние ключи для проверки
    if set(stolcat_keys).issubset(csv_keys):
        outtxt += "<br>" + str(csv_keys) + " = " + str(stolcat_keys) + "OK(cat)-Файл готов к импорту!"
    else:
        outtxt = str(csv_keys) + " = " + str(stolcat_keys) + "FAIL(cat)-файл неправильный!"
        return HttpResponse(outtxt) #отсутствуют данные по таблице льгот
    #############################начинаем проверку соответствия данных имеющейсся базе#######################
    diffout = ""
    tableout = tablib.Dataset(headers=csv_keys)

    totalup=0
    totalupids=[]
    stolcat = set(stolovayacategory.objects.all())

    for csv_row in csv_data:
        anyoneup=0
        for qs_row in modelstol.objects.all():
            if csv_row['id'] == '':
                continue
            if int(csv_row['id']) == int(qs_row.id):
#                tabletmp = list(val for key, val in csv_row.items())
#                tabletmp = dict({key:val for key, val in csv_row.items()})
                upflag=0
                upflag2=0
                anyoneup=1
                tabletmp = copy.copy(csv_row)
                tablerw = copy.copy(csv_row)
                #category
#                tablerw['category'] = tolcategoryget(qs_row, datasek, stolcat)
#                tablerwtmp['category'] = tablerw['category']
                qs_cat = stolcategoryget(qs_row, datasek, stolcat)
                #category
                if str(csv_row['classname']) != str(qs_row.classname):
                    tabletmp['classname'] = str(qs_row.fio) + " => " + str(csv_row['classname'])
                    tablerw['classname'] =  csv_row['classname']
                    upflag=1
                if str(csv_row['fio']) != str(qs_row.fio):
                    tabletmp['fio'] = str(qs_row.fio) + " => " + str(csv_row['fio'])
                    tablerw['fio'] =  csv_row['fio']
                    upflag=1
                if str(csv_row['internat']) != str(qs_row.internat):
                    tabletmp['internat'] = str(qs_row.internat) + " => " + str(csv_row['internat'])
                    tablerw['internat'] =  csv_row['internat']
                    upflag=1
                if str(csv_row['pitendatedi']) != str(qs_row.pitendatedi):
                    tabletmp['pitendatedi'] = str(qs_row.pitendatedi) + " => " + str(csv_row['pitendatedi'])
                    tablerw['pitendatedi'] =  csv_row['pitendatedi']
                    upflag=1
                if str(csv_row['pitendateen']) != str(qs_row.pitendateen):
                    tabletmp['pitendateen'] = str(qs_row.pitendateen) + " => " + str(csv_row['pitendateen'])
                    tablerw['pitendateen'] =  csv_row['pitendateen']
                    upflag=1
                if str(csv_row['qrcode']) != str(qs_row.qrcode):
                    if qs_row.qrcode != None:
                        tabletmp['qrcode'] = str(qs_row.qrcode) + " => " + str(csv_row['qrcode'])
                        tablerw['qrcode'] =  csv_row['qrcode']
                        upflag=1
                if str(csv_row['category']) != str(qs_cat.typeofeda):
                    tabletmp['category'] = str(qs_cat.typeofeda) + " => " + str(csv_row['category'])
                    tablerw['category'] =  csv_row['category']
                    upflag2=1
                tableout.append(tabletmp.values())

                if upflag > 0 or upflag2 > 0:
                    totalup += 1
                    totalupids.append(tabletmp['id'])
                    tablerwmain = copy.copy(tablerw)
                    if upflag > 0:
                        if submitok == 1:
                            tarobject = modelstol.objects.filter(id=tabletmp['id']) 
                            tarobject.update(classname=tablerwmain['classname'],fio = tablerwmain['fio'],internat = tablerwmain['internat'],pitendateen = tablerwmain['pitendateen'],pitendatedi = tablerwmain['pitendatedi'],qrcode = tablerwmain['qrcode'])
                    if upflag2 > 0:
                        if submitok == 1:
                            stolovayacategory(uchid_id=tabletmp['id'], category=tablerwmain['category'], dateeda=datasek, datetime1=datetime.now()).save()
                continue
        #если никого нет и нечего обновлять
        if anyoneup == 0:
            tabletmp = copy.copy(csv_row)
            if modelstol.objects.filter(classname=csv_row['classname'],fio = csv_row['fio'],internat = csv_row['internat'],pitendateen = csv_row['pitendateen'],pitendatedi = csv_row['pitendatedi'],qrcode = csv_row['qrcode']).count() <= 0: #если в файле неправильный id
                totalup += 1
                tabletmp['id'] = tabletmp['id'] + "-NEW"
                if submitok == 1:
                    try:
                        tarobject2 = modelstol.objects.create(id=csv_row['id'], classname=csv_row['classname'],fio = csv_row['fio'],internat = csv_row['internat'],pitendateen = csv_row['pitendateen'],pitendatedi = csv_row['pitendatedi'],qrcode = csv_row['qrcode'])
                    except:
                        tarobject2 = modelstol.objects.create(classname=csv_row['classname'],fio = csv_row['fio'],internat = csv_row['internat'],pitendateen = csv_row['pitendateen'],pitendatedi = csv_row['pitendatedi'],qrcode = csv_row['qrcode'])
#                    tarobject2 = modelstol.objects.filter(classname=csv_row['classname'],fio = csv_row['fio'],internat = csv_row['internat'],pitendateen = csv_row['pitendateen'],pitendatedi = csv_row['pitendatedi'],qrcode = csv_row['qrcode'])[0]
                    stolovayacategory.objects.create(uchid_id=tarobject2.id, category=csv_row['category'], dateeda=datetime(2020, 1, 1 ,1 ,1 ,1, 1).date(), datetime1=datetime.now())
                    totalupids.append(tarobject2.id)
                    if csv_row['id'] == '':
                        tabletmp['id'] = str(csv_row['id']) + "-NEW другим ID " + str(tarobject2.id)
                    else:
                        if int(tarobject2.id) == int(csv_row['id']):
                            tabletmp['id'] = str(csv_row['id']) + "-NEW с таки же ID " + str(tarobject2.id)
                        else:
                            tabletmp['id'] = str(csv_row['id']) + "-NEW другим ID " + str(tarobject2.id)
                else:
                    totalupids.append(csv_row['id'])
            else: #такой ученик уже есть
                tarobject2 = modelstol.objects.filter(classname=csv_row['classname'],fio = csv_row['fio'],internat = csv_row['internat'],pitendateen = csv_row['pitendateen'],pitendatedi = csv_row['pitendatedi'],qrcode = csv_row['qrcode'])[0]
                if int(tarobject2.id) == int(csv_row['id']):
                    tabletmp['id'] = str(csv_row['id']) + "-с таки же ID " + str(tarobject2.id)
                else:
                    tabletmp['id'] = str(csv_row['id']) + "-другим ID(Исправь) " + str(tarobject2.id)
            tableout.append(tabletmp.values())


    return HttpResponse(outtxt + "<br>" + "Всего будет обновлено:" + str(totalup) + "<br> id=" + str(totalupids) + "<br>" + str(submitok) + "<br>" + str(tableout.html))



@login_required
def importexport(request): #ViewINDEX
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
    datasek = datetime.now().strftime("%Y-%m-%d")
    exformat = ""
    filedl = 0
    imexproc = 0
    if request.method == 'GET' and request.GET:
        dicta = dict(request.GET)
        if dicta.get('import',0) !=0: #Import
            if dicta.get('export',0) !=0: #Export
                del dicta['export']
            del dicta['import']
            del dicta['csrfmiddlewaretoken']
            imexproc = 1
        if dicta.get('export',0) !=0: #Export
            if dicta.get('import',0) !=0:
                del dicta['import']
            del dicta['export']
            del dicta['csrfmiddlewaretoken']
            imexproc = 2
            if dicta.get('format', 0) != 0:
                exformat = dicta.get('format')[0]
                del dicta['format']
                if exformat=="nothing" or exformat == "":
                    exformat="csv"
            if dicta.get('datepicker', 'nothing1') == 'nothing1':
                datasek = datetime.now().strftime("%Y-%m-%d")
            else:
                datasek = dicta.get('datepicker')[0]
                del dicta['datepicker']
            if dicta.get('filedl', 99) == 99:
                pass
            else:
                filedl = int(dicta.get('filedl', 0)[0])
                del dicta['filedl']
    if filedl == 1: #Fileok
        filename = 'export%s.csv' % str(datasek)
        filedownload = HttpResponse(content_type="text/csv")
        filedownload['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
        filedownload = getdataex(datasek, filedownload)
        return filedownload
    context = {'usergr':unique_groups, 'datasek':datasek, 'exformat':exformat, 'filedl':filedl, 'imexproc':imexproc}
    return render(request, 'stolovaya/importexport/index.html', context)


def getdataex(datasek, filedownload):
    stolovayaopts = modelstol._meta
    stolovayamodel = modelstol
    stolcat = set(stolovayacategory.objects.all())
    field_names = [field.name for field in stolovayaopts.fields]
    field_names_txt = field_names.copy()
    #####additional-head##########
    field_names_txt.append("category")
    #####additional-head##########
    writer = csv.writer(filedownload)
    writer.writerow(field_names_txt)
    for obj in stolovayamodel.objects.all():
        datarowex=[getattr(obj, field) for field in field_names]
        #######additional-obj#############
#        datarowex.append("normal")
        datarowex.append(stolcategoryget(obj,datasek,stolcat).typeofeda)
        #######additional-obj#############
        writer.writerow(datarowex)
    return filedownload

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
    if len(list(filter(lambda x:x.uchid_id==stolm.id,stolcat))) <= 0:
        stolm.typeofeda = 'normal'
    return stolm
