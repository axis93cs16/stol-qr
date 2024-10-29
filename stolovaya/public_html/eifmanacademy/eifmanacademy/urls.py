"""eifmanacademy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap
from cms.sitemaps import CMSSitemap
#from filebrowser_safe import urls as urlsite
from filebrowserplugin.views import view_locale
from filebrowser.sites import site as fbsite
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [
    re_path(r'^admin/filebrowser/', fbsite.urls),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include('stolovaya.urls')),
    re_path(r'^', include('cms.urls')),
#    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'favicon.ico$',RedirectView.as_view(url='/static/favicon.ico'),name='favicon'),
    re_path(r'robots.txt$', TemplateView.as_view(template_name='robots.txt'),name='robots.txt'),


#    re_path('grappelli/', include('grappelli.urls')),
#    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
#    re_path(r'^locale.loc$', view_locale),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +  staticfiles_urlpatterns()
