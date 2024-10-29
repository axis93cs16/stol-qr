# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from datetime import datetime

def get_typesofeda():
    returnvar = [
        ('normal',_('normal')),
        ('lgota14',_('lgota14')),
        ('lgota59',_('lgota59')),
        ('internat14',_('internat14')),
        ('internat59',_('internat59')),
        ('dogovor1',_('dogovor1')),
        ('dogovor2',_('dogovor2')),
        ('dogovor3',_('dogovor3')),
        ('internatp',_('internatp')),
    ]
    return returnvar

def get_typesofinternat():
    returnvar = [
        ('normal',_('normal')),
        ('2-level',_('2-level')),
        ('3-level',_('3-level')),
        ('4-level',_('4-level')),
    ]
    return returnvar


class stolovaya(models.Model):
#    iduch = models.Int(iduch, on_delete = models.CASCADE)
    classname = models.CharField(
        verbose_name=_('Group'),
        max_length=255,
        blank = False
    )
    fio = models.CharField(_('fio'), max_length=255, blank=False)
#    typeofeda = models.CharField(_('typeofeda'), max_length=255, choices=get_typesofeda(), default=get_typesofeda()[0][0], blank=False)

    _sortable_fields = (
        ('classname', _('classname')),
        ('fio', _('fio')),
        ('typeofeda', _('typeofeda')),
        ('internat', _('internat')),
    )
    internat = models.CharField(_('internat'), max_length=255, choices=get_typesofinternat(), default=get_typesofinternat()[0][0], blank=False)
#    medflag = models.BooleanField(
#        verbose_name=_('medcenter'),
#        default = False
#    )
    pitendatedi = models.DateField(
        verbose_name=_('Pitanie_po_menu_s'),
        default = datetime(2030, 1, 1 ,1 ,1 ,1, 1)
    )
    pitendateen = models.DateField(
        verbose_name=_('Pitanie_po_menu_po'),
        default = datetime(2001, 1, 1 ,1 ,1 ,1, 1)
    )
    qrcode = models.CharField(
        verbose_name=_('QR_Code'),
        blank=True,
        null=True,
        default = None,
        max_length = 255,
    )
    @classmethod
    def get_sortable_fields(cls):
        return cls._sortable_fields

    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
#    cmsplugin_ptr = models.OneToOneField(
#        CMSPlugin,
#        related_name='%(app_label)s_%(class)s',
#        parent_link=True,
#        on_delete=models.CASCADE,
#    )

    class Meta:
#        managed = False
#        abstract = True
        ordering = ['classname',
                    'fio',
                    ]
        verbose_name = _("Stolovaya")
        verbose_name_plural = _("Stolovaya")



    def __str__(self):
        return str(self.classname)+' - '+str(self.fio) + '(' + str(self.id) + ')'



class stolovayainfodata(models.Model):
    datapit = models.DateField(
        verbose_name=_('datapitaniya'),
        blank = False
    )
#    uchid = models.IntegerField(
#        verbose_name=_('id_uchenika'),
#        blank = False
#    )
    id = models.ForeignKey(
        stolovaya,
        name = 'uchid',
        verbose_name = _('id_uchenika'),
#        blank = False,
        on_delete = models.CASCADE,
    )

    chkflag = models.BooleanField(
        verbose_name=_('checked'),
    )
    datazapis = models.DateTimeField(
        verbose_name=_('datazapis'),
        blank = True
    )
    def __str__(self):
        return str(self.datapit) + ' - ' + str(self.uchid)

class stolovayainfopit(models.Model):
    datapit = models.DateField(
        verbose_name=_('datapitaniya'),
        blank = False
    )
    id = models.ForeignKey(
        stolovaya,
        name = 'uchid',
        verbose_name = _('id_uchenika'),
#        blank = False,
        on_delete = models.CASCADE,
    )
    zavtrak = models.BooleanField(
        verbose_name=_('z_checked'),
        blank=True,
        null=True
        )
    obed = models.BooleanField(
        verbose_name=_('o_checked'),
        blank=True,
        null=True
        )
    poldnik = models.BooleanField(
        verbose_name=_('p_checked'),
        blank=True,
        null=True
        )
    ujin1 = models.BooleanField(
        verbose_name=_('u1_checked'),
        blank=True,
        null=True
        )
    ujin2 = models.BooleanField(
        verbose_name=_('u2_checked'),
        blank=True,
        null=True
        )
    obedk = models.BooleanField(
        verbose_name=_('kompleks_checked'),
        blank=True,
        null=True
        )
    obedkg1 = models.BooleanField(
        verbose_name=_('dogovor_1_checked'),
        blank=True,
        null=True
        )
    obedkg2 = models.BooleanField(
        verbose_name=_('dogovor_2_checked'),
        blank=True,
        null=True
        )
    obedkg3 = models.BooleanField(
        verbose_name=_('dogovor_3_checked'),
        blank=True,
        null=True
        )
    zavtrakg = models.BooleanField(
        verbose_name=_('zavtrak_g_checked'),
        blank=True,
        null=True
        )
    internatp = models.BooleanField(
        verbose_name=_('internatp'),
        blank=True,
        null=True
        )

    datapittime = models.DateTimeField(
            verbose_name=_('datazapis'),
            blank = True
        )
    forceflagz = models.DateTimeField(
        verbose_name=_('force_checked_z'),
        default = None,
        blank=True,
        null=True
        )
    forceflago = models.DateTimeField(
        verbose_name=_('force_checked_o'),
        default = None,
        blank=True,
        null=True
        )
    forceflagp = models.DateTimeField(
        verbose_name=_('force_checked_p'),
        default = None,
        blank=True,
        null=True
        )
    forceflagu1 = models.DateTimeField(
        verbose_name=_('force_checked_u1'),
        default = None,
        blank=True,
        null=True
        )
    forceflagu2 = models.DateTimeField(
        verbose_name=_('force_checked_u2'),
        default = None,
        blank=True,
        null=True
        )
    forceflagok = models.DateTimeField(
        verbose_name=_('force_checked_ok'),
        default = None,
        blank=True,
        null=True
        )
    forceflagokg1 = models.DateTimeField(
        verbose_name=_('force_checked_okg1'),
        default = None,
        blank=True,
        null=True
        )
    forceflagokg2 = models.DateTimeField(
        verbose_name=_('force_checked_okg2'),
        default = None,
        blank=True,
        null=True
        )
    forceflagokg3 = models.DateTimeField(
        verbose_name=_('force_checked_okg3'),
        default = None,
        blank=True,
        null=True
        )
    forceflagozg = models.DateTimeField(
        verbose_name=_('force_checked_ozg'),
        default = None,
        blank=True,
        null=True
        )
    forceflagip = models.DateTimeField(
        verbose_name=_('force_checked_ip'),
        default = None,
        blank=True,
        null=True
        )

    forceflagmed = models.DateTimeField(
        verbose_name=_('force_checked_med'),
        default = None,
        blank=True,
        null=True
        )




    class Meta:
        get_latest_by = 'datapittime'

class stolovayainfopitafter(models.Model):
    datapit = models.DateField(
        verbose_name=_('datapitaniya'),
        blank = False
    )
    id = models.ForeignKey(
        stolovaya,
        name = 'uchid',
        verbose_name = _('id_uchenika'),
#        blank = False,
        on_delete = models.CASCADE,
        )
    zavtrak = models.BooleanField(
        verbose_name=_('z_checked'),
        blank=True,
        null=True
        )
    obed = models.BooleanField(
        verbose_name=_('o_checked'),
        blank=True,
        null=True
        )
    poldnik = models.BooleanField(
        verbose_name=_('p_checked'),
        blank=True,
        null=True
        )
    ujin1 = models.BooleanField(
        verbose_name=_('u1_checked'),
        blank=True,
        null=True
        )
    ujin2 = models.BooleanField(
        verbose_name=_('u2_checked'),
        blank=True,
        null=True
        )
    obedk = models.BooleanField(
        verbose_name=_('kompleks_checked'),
        blank=True,
        null=True
        )
    obedkg1 = models.BooleanField(
          verbose_name=_('obedkg1_checked'),
          blank=True,
          null=True
        )
    obedkg2 = models.BooleanField(
          verbose_name=_('obedkg2_checked'),
          blank=True,
          null=True
        )
    obedkg3 = models.BooleanField(
          verbose_name=_('obedkg3_checked'),
          blank=True,
          null=True
        )
    zavtrakg = models.BooleanField(
          verbose_name=_('zavtrakg_checked'),
          blank=True,
          null=True
        )
    internatp = models.BooleanField(
          verbose_name=_('internatp_checked'),
          blank=True,
          null=True
        )

    datapittime = models.DateTimeField(
            verbose_name=_('datazapis'),
            blank = True
        )

class stolovayapodacha(models.Model):
    zavtrak = models.TimeField(
          verbose_name=_('zavtrak'),
          default="07:30:00"
        )
    obed = models.TimeField(
          verbose_name=_('obed'),
          default="09:15:00"
        )
    poldnik = models.TimeField(
          verbose_name=_('poldnik'),
          default="09:15:00"
        )
    ujin1 = models.TimeField(
          verbose_name=_('ujin1'),
          default="09:15:00"
        )
    ujin2 = models.TimeField(
          verbose_name=_('ujin2'),
          default="09:15:00"
        )
    obedk = models.TimeField(
          verbose_name=_('obedk'),
          blank=True,
          null=True,
          default="09:15:00"
        )
    obedkg1 = models.TimeField(
          verbose_name=_('obedkg1'),
          blank=True,
          null=True,
          default="09:15:00"
        )
    obedkg2 = models.TimeField(
          verbose_name=_('obedkg2'),
          blank=True,
          null=True,
          default="09:15:00"
        )
    obedkg3 = models.TimeField(
          verbose_name=_('obedkg3'),
          blank=True,
          null=True,
          default="09:15:00"
        )
    zavtrakg = models.TimeField(
          verbose_name=_('zavtrakg'),
          blank=True,
          null=True,
          default="07:30:00"
        )
    site = models.OneToOneField(Site, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+' - '+str(self.site) + '(З=' + str(self.zavtrak) + ' О=' + str(self.obed) + ' П=' + str(self.poldnik) + ' У1=' + str(self.ujin1) + ' У2=' + str(self.ujin2) + ')'


class stolovayapriemipishi(models.Model):
    zavtrak = models.TimeField(
          verbose_name=_('zavtrak'),
          default="07:31:00"
        )
    obed = models.TimeField(
          verbose_name=_('obed'),
          default="09:30:00"
        )
    poldnik = models.TimeField(
          verbose_name=_('poldnik'),
          default="09:30:00"
        )
    ujin1 = models.TimeField(
          verbose_name=_('ujin1'),
          default="09:30:00"
        )
    ujin2 = models.TimeField(
          verbose_name=_('ujin2'),
          default="09:30:00"
        )
    obedk = models.TimeField(
          verbose_name=_('obedk'),
          blank=True,
          null=True
        )
    obedkg1 = models.TimeField(
          verbose_name=_('obedkg1'),
          blank=True,
          null=True,
          default="09:30:00"
        )
    obedkg2 = models.TimeField(
          verbose_name=_('obedkg2'),
          blank=True,
          null=True,
          default="09:30:00"
        )
    obedkg3 = models.TimeField(
          verbose_name=_('obedkg3'),
          blank=True,
          null=True,
          default="09:30:00"
        )
    zavtrakg = models.TimeField(
          verbose_name=_('zavtrakg'),
          blank=True,
          null=True,
          default="09:30:00"
        )

    site = models.OneToOneField(Site, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+' - '+str(self.site) + '(З=' + str(self.zavtrak) + ' О=' + str(self.obed) + ' П=' + str(self.poldnik) + ' У1=' + str(self.ujin1) + ' У2=' + str(self.ujin2) + ')'

def get_typesoftalon():
    returnvar = [
        ('obed1',_('obed2')),
        ('obed2',_('obed2')),
        ('obed3',_('obed3')),
        ('internatp',_('internatp'))
    ]
    return returnvar


class stolovayatalon(models.Model):
    datetime1 = models.DateTimeField(
        verbose_name=_('DateTime_otmetka'),
#        default = None,
        blank=False,
#        null=True
        )
    dateeda = models.DateField(
        verbose_name=_('Date_pitania'),
#        default = None,
        blank=False,
#        null=True
        )
    catoftalon = models.CharField(_('catoftalon'), max_length=255, choices=get_typesoftalon(), default=get_typesoftalon()[0][0], blank=False)
    numoftalons = models.IntegerField(
        verbose_name=_('numoftalons'),
        blank = False
    )
    def __str__(self):
        return str(self.id) +' - талон от' + str(self.datetime1) + 'на'+ str(self.dateeda)
    pass

class stolovayacategory(models.Model):
    datetime1 = models.DateTimeField(
        verbose_name=_('DateTime_otmetka'),
#        default = None,
        blank=False,
#        null=True
        )
    dateeda = models.DateField(
        verbose_name=_('Date_pitania'),
#        default = None,
        blank=False,
#        null=True
        )
    category = models.CharField(_('typeofeda'), max_length=255, choices=get_typesofeda(), default=get_typesofeda()[0][0], blank=False)

    id = models.ForeignKey(
        stolovaya,
        name = 'uchid',
        verbose_name = _('id_uchenika'),
#        blank = False,
        on_delete = models.CASCADE,
    )
    xvarx = models.IntegerField(
        verbose_name=_('multiplier'),
        default=1,
        blank=False,
    )

    pass

class stolovayamedflag(models.Model):
    datetime1 = models.DateTimeField(
        verbose_name=_('DateTime_otmetka'),
#        default = None,
        blank=False,
#        null=True
        )
    dateeda = models.DateField(
        verbose_name=_('Date_pitania'),
#        default = None,
        blank=False,
#        null=True
        )
    medflag = models.BooleanField(
        verbose_name=_('medcenter'),
        default = False
    )

    id = models.ForeignKey(
        stolovaya,
        name = 'uchid',
        verbose_name = _('id_uchenika'),
#        blank = False,
        on_delete = models.CASCADE,
    )

    pass
#stolovaya.stolovayainfodata_set

class stolovayaclasspit(models.Model):
    classname = models.CharField(
        verbose_name=_('Group'),
        max_length=255,
        blank = False,
        primary_key=True
    )
    zavtrak = models.TimeField(
          verbose_name=_('zavtrak'),
        )
    obed = models.TimeField(
          verbose_name=_('obed'),
        )
    poldnik = models.TimeField(
          verbose_name=_('poldnik'),
        )
    ujin1 = models.TimeField(
          verbose_name=_('ujin1'),
        )
    ujin2 = models.TimeField(
          verbose_name=_('ujin2'),
        )
    obedk = models.TimeField(
          verbose_name=_('obedk'),
          blank=True,
          null=True
        )
    obedkg1 = models.TimeField(
          verbose_name=_('obedkg1'),
          blank=True,
          null=True
        )
    obedkg2 = models.TimeField(
          verbose_name=_('obedkg2'),
          blank=True,
          null=True
        )
    obedkg3 = models.TimeField(
          verbose_name=_('obedkg3'),
          blank=True,
          null=True
        )


    def __str__(self):
        return str(self.classname)
    pass

class stolovayafactstol(models.Model):
    id = models.ForeignKey(
        stolovaya,
        name = 'uchid',
        verbose_name = _('id_uchenika'),
        on_delete = models.CASCADE,
    )
    datetime = models.DateTimeField(
        verbose_name=_('DateTime_otmetka'),
        blank=False,
        )
    dateeda = models.DateField(
        verbose_name=_('Date_pitania'),
        blank=False,
        )
    typeofedapit = models.CharField(
        verbose_name=_('type_of_eda_pit'),
        blank=True,
        null=True,
        default = None,
        max_length = 255,
    )
    pass

class stolovayablkdata(models.Model):
    datetime1 = models.DateTimeField(
        verbose_name=_('DateTime_otmetka'),
#        default = None,
        blank=False,
#        null=True
        )
    dateeda = models.DateField(
        verbose_name=_('Date_pitania'),
#        default = None,
        blank=False,
#        null=True
        )
    blockflag = models.BooleanField(
        verbose_name=_('blocked'),
        default = False
    )

    id = models.ForeignKey(
        stolovaya,
        name = 'uchid',
        verbose_name = _('id_uchenika'),
#        blank = False,
        on_delete = models.CASCADE,
    )

    pass


class stolovayadietflag(models.Model):
    datetime1 = models.DateTimeField(
        verbose_name=_('DateTime_otmetka'),
#        default = None,
        blank=False,
#        null=True
        )
    dateeda = models.DateField(
        verbose_name=_('Date_pitania'),
#        default = None,
        blank=False,
#        null=True
        )
    dietflag = models.BooleanField(
        verbose_name=_('dieta'),
        default = False
    )

    id = models.ForeignKey(
        stolovaya,
        name = 'uchid',
        verbose_name = _('id_uchenika'),
#        blank = False,
        on_delete = models.CASCADE,
    )

    pass