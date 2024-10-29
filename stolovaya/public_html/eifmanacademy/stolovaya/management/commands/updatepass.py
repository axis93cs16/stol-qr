from django.core.management.base import BaseCommand
#from django.utils import simplejson
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from stolovaya.models import stolovaya as modelstol
import random

#@login_required
#def changepasswords(request):
#    if not request.user.groups.values_list('name',flat = True):
#        return redirect('/login/?next=%s' % request.path)
#    else:
#        flagen=0
#        avilgr=['stol-admin']
#        unique_groups = set( val for dic in request.user.groups.all().values('name') for val in dic.values())
#        for i in avilgr:
#            for j in unique_groups:
#                if str(i)==str(j):
#                    flagen=1
#                    break
#        if flagen==0 :
#            return redirect('/login/?next=%s' % request.path)
class Command(BaseCommand):
    help = "try to print datetime"
    def handle(self, *args, **kwargs):

#    okflag = 1
#    if request.method == 'POST' and request.POST:
#        dicta = dict(request.POST)
#        if dicta.get('formupda',0) !=0: #ok
#            del dicta['formupda']
#            del dicta['csrfmiddlewaretoken']
#            okflag = 1
#        else:
#            okflag = 0
#    if okflag == 0:
#        result="<form>{% csrf_token %}</form>"
#        return HttpResponse(result)
#    if okflag == 1:
        try:
            queryset = modelstol.objects.all().order_by('classname','fio')
            lgotaarrlist2 = queryset.values('classname')
            list_of_unique_class = {}#[]
            unique_class = sorted(set( val for dic in lgotaarrlist2 for val in dic.values()))
            idcl=0
        #    list_of_unique_class.update({idcl:'Все'})
        #    idcl=1
            for class2 in unique_class:
        #        if str('stol-admin') in unique_groups:
        #            list_of_unique_class.update({idcl:class2})#idcl:class2})
        #            idcl+=1
        #        else:
        #        if str(class2) in unique_groups:
                list_of_unique_class.update({idcl:class2})#idcl:class2})
                idcl+=1
            selectitems2 = list_of_unique_class
    
    
            from django.contrib.auth.models import Group, User
        #    result = {}
            result = ""
            for itofcl in selectitems2.values():
                if itofcl == 'Все':
                    continue
                passworduser = "!"+itofcl+'!s'+ str(random.randrange(0, 9, 1))
                try:
                    user = User.objects.get(username=(itofcl+'-ruk'))
                    user.set_password(passworduser)
                    user.save()
                    result=result+"=ok="
                except:
                    user = User.objects.create_user(username=(itofcl+'-ruk'), password=(passworduser))
                result = result + "user: " + itofcl + '-ruk' + " password: " + passworduser + "\n"
                #result.a"{{'user': '" + itofcl + '-ruk' + "'}:{'password': '" + passworduser + "'}},"
    
                new_group, created = Group.objects.get_or_create(name=itofcl)
                new_group.user_set.add(user)
                my_group = Group.objects.get(name='class-ed')
                my_group.user_set.add(user)
        #    return HttpResponse(result, content_type='application/json')
        #    result= result + "}"
            self.stdout.write(result)
        except Exception as e:
            self.stdout.write(f"error: {e}")
#            return HttpResponse(result)