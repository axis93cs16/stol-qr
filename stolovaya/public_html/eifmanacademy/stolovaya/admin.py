# coding=utf-8
from django.contrib import admin
from stolovaya.models import stolovaya, stolovayapodacha, stolovayapriemipishi, stolovayacategory, stolovayaclasspit,  stolovayainfodata
from django.utils.translation import ugettext as _
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from datetime import datetime
from django.apps import apps
from django.db import models
import tablib
import collections
from django.db.backends.base import schema

class listfilterforme(ImportExportModelAdmin):
#    list_filter = ('classname', 'typeofeda')
#    list_display = ('classname', 'fio', 'typeofeda')
    list_filter = ('classname', 'internat')
    list_display = ('classname', 'fio',  'internat', 'my_field')
    
    #@admin.display(description=_("Column title"))
    def my_field(self, obj):
        typeofeda = 'normal'
        tmpfdatpit = datetime.now().date()
        tmpdatpit = datetime(2020, 1, 1 ,1 ,1 ,1, 1).date()
        tmpfdatpittime = datetime(2020, 1, 1 ,1 ,1 ,1, 1)
        for objcat in stolovayacategory.objects.filter(uchid_id=obj.id):
            if objcat.dateeda >= tmpdatpit:
                tmpdatpit = objcat.dateeda
                if tmpfdatpit >= objcat.dateeda :
                    if objcat.datetime1.timestamp() >= tmpfdatpittime.timestamp():
                        tmpfdatpittime = objcat.datetime1
                        typeofeda = objcat.category
        return typeofeda
    my_field.allow_tags = True
    my_field.short_description = 'typeofeda'

class listfilterforme2(ImportExportModelAdmin):
#    list_filter = ('category')
    list_display = ('category', 'uchid_id',  'dateeda', 'datetime1' )
    pass
#class adminext():
 

#@admin.register(Comment)
#class CommentAdmin(ImportExportModelAdmin):
#    pass
#class stolovayainfo(admin.ModelAdmin):
#    verbose_name = '111'
#    verbose_name_plural = '111'
#    queryset = stolovaya.objects.filter('classname')
#
#    class Meta:
#        def __str__(self):
#            return verbose_name
#    return queryset

class saveastrue(admin.ModelAdmin):
    save_as = True
    pass
admin.site.register(stolovaya, listfilterforme)
admin.site.register(stolovayapodacha)
admin.site.register(stolovayapriemipishi)
admin.site.register(stolovayaclasspit, saveastrue)
admin.site.register(stolovayacategory, listfilterforme2)
admin.site.register(stolovayainfodata)




#class StudentsBaseAdmin(ImportExportModelAdmin):
#    resource_class = StudentsBase

#admin.site.register(stolovaya, StudentsBaseAdmin)