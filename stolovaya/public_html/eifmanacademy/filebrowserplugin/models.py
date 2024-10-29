# coding=utf-8
from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext as _
from filebrowser.fields import FileBrowseField
from djangocms_attributes_field.fields import AttributesField
from django.conf import settings


LINK_TARGET = (
    ('_self', _('Open in same window')),
    ('_blank', _('Open in new window')),
    ('_parent', _('Delegate to parent')),
    ('_top', _('Delegate to top')),
)

def get_templates():
    choices = [
        ('default', _('Default')),
    ]
    choices += getattr(
        settings,
        'DJANGOCMS_FBP_TEMPLATES',
        [],
    )
    return choices

class FilePlugin(CMSPlugin):
    template = models.CharField(
        verbose_name=_('Template'),
        choices=get_templates(),
        default=get_templates()[0][0],
        max_length=255,
    )



    title = models.CharField(_('title'), max_length=255, blank=False)
    link = FileBrowseField(_('link'), max_length=255, blank=False)

    link_target = models.CharField(
        verbose_name=_('Link target'),
        choices=LINK_TARGET,
        blank=True,
        max_length=255,
        default='_blank',
    )
    showsize = models.BooleanField(_('showsize'), default=True)
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
        excluded_keys=['href', 'title', 'target'],
    )

    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
        on_delete=models.CASCADE,
    )

#    class Meta:
#        abstract = True

    def __str__(self):
        return self.title

