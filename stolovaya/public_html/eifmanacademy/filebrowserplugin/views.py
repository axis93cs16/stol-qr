import locale
import sys
from django.http import HttpResponse
from datetime import datetime
from django.utils.timezone import now as dnow

def view_locale(request):
    loc_info = "getlocale: " + str(locale.getlocale()) + \
        "<br/>getdefaultlocale(): " + str(locale.getdefaultlocale()) + \
        "<br/>fs_encoding: " + str(sys.getfilesystemencoding()) + \
        "<br/>sys default encoding: " + str(sys.getdefaultencoding()) + \
        "<br/>" + str(dnow()) + \
        "<br/>" + str(datetime.now())
#        printenv()
    return HttpResponse(loc_info)
