# coding=utf-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import FilePlugin
from django.utils.translation import ugettext_lazy as _


#@plugin_pool.register_plugin
class filebrowserplugin(CMSPluginBase):
    name = _("LinkToFile")
    model = FilePlugin
    module = "FileBrowser"
#    render_template = "filebrowserplugin/default/filefromlink.html"
    allow_children = False
    text_enabled = True
    def get_render_template(self, context, instance, placeholder):
        return 'filebrowserplugin/{}/file.html'.format(instance.template)

plugin_pool.register_plugin(filebrowserplugin)


