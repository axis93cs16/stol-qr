# coding=utf-8
from django.urls import re_path, include
#from django.conf.urls import include
#from contacts.views import ContactsView, ThanksView
from .views import AdminViewme, AdminViewstol, AdminViewmeint, form_test, form_test2, AdminViewmemed, AdminViewmeka, form_test3, form_test4, form_test5, form_test6, form_test7, form_testf, AdminViewmeKor, form_testfkor, AdminReport,  Scanviewer, scanscan, qrcodeview, stoladminqr, indexpage, AdminKanikuls, AdminKanikuls2, stoladminqrreport1, AdminEndOfYear, AdminEndOfYear2
from .views import AdminViewmeblk, AdminViewmediet
#from .utility import api_gb_stol_show
from .importexport import importexport, getfilecsv #FileUploadView
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from cms.apphook_pool import apphook_pool
from django.contrib.auth.decorators import login_required

app_name= 'stolovaya'

if apphook_pool.get_apphooks():
    # If there are some application urls, use special resolver,
    # so we will have standard reverse support.
    urlpatterns = get_app_patterns()
else:
    urlpatterns = []

urlpatterns = [
    re_path('modal/', form_test, name='form_test'),
    re_path('modal2/', form_test2, name='form_test2'),
    re_path('modal3/', form_test3, name='form_test3'),
    re_path('modal4/', form_test4, name='form_test4'),
    re_path('modal5/', form_test5, name='form_test5'),
    re_path('modalf/', form_testf, name='form_testf'),
    re_path('modalfkor/', form_testfkor, name='form_testfkor'),
    re_path('modal6/', form_test6, name='form_test6'),
    re_path('modal7/', form_test7, name='form_test7'),
    re_path('scanscan/', scanscan, name='scanscan'),
#    re_path('api_gb_stol/', api_gb_stol_show.as_view()),
#    re_path('fileuploadtome/', FileUploadView.as_view(), name='fileuploadtome')
    re_path('fileuploadtome/', getfilecsv, name='fileuploadtome')

]


urlpatterns.extend([
#   url(r"^$", ContactsView.as_view(), name="contacts_index"),
    re_path(r"classadmin$", AdminViewme, name="adminclass_page"),
    re_path(r"stoladmin$", AdminViewstol, name="adminstol_page"),
    re_path(r"intadmin$", AdminViewmeint, name="adminint_page"),
    re_path(r"medadmin$", AdminViewmemed, name="adminmed_page"),
    re_path(r"adminka$", AdminViewmeka, name="adminka_page"),
    re_path(r"korrekt$", AdminViewmeKor, name="adminkor_page"),
    re_path(r"report$", AdminReport, name="adminreport_page"),
    re_path(r"kanikuls$", AdminKanikuls, name="adminkanikuls_page"),
    re_path(r"kanikul2$", AdminKanikuls2, name="adminkanikuls2a_page"),
    re_path(r"endofyears$", AdminEndOfYear, name="adminendofyear_page"),
    re_path(r"endofyear2$", AdminEndOfYear2, name="adminendofyear2_page"),
    re_path(r"blkadmin$", AdminViewmeblk, name="adminblkmanage_page"),
    re_path(r"dietadmin$", AdminViewmediet, name="admindietmanage_page"),

    re_path('login/', auth_views.LoginView.as_view(template_name='stolovaya/login.html'), name='login'),
#    re_path('accounts/', include('django.contrib.auth.urls')),
    re_path('logout/', auth_views.LogoutView.as_view(template_name='stolovaya/logout.html'), name='logout'),
    re_path(r'index$', indexpage, name='index'),
    #re_path(r'^$', indexpage, name='index'),
    re_path(r'scanner$', Scanviewer, name="scanviewer_page" ),
    re_path(r'qrcodes$', qrcodeview, name="qrcodeview"),
    re_path(r'stoladminqr$', stoladminqr, name='stoladminqr'),
    re_path(r'stoladminqrr1$', stoladminqrreport1, name='stoladminqrr1'),
    re_path(r'importexport$', importexport, name='importexport'),
#    re_path(r'qr_code/', include('qr_code.urls', namespace="qr_code")),
#    re_path('export-data/', export_data, name="export_data"),
#    re_path('ajax/', include('ajax.urls'))
#    re_path(r'^stolovaya/import/$', login_required(views.MyModelImportView.as_view()), name='mymodel_import'),
#    re_path(r'^stolovaya/import/confirm/$', login_required(views.MyModelImportView.as_view(confirm=True)), name='mymodel_import_confirm'),
   ])
