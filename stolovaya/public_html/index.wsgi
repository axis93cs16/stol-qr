import os
import sys
from datetime import datetime
#import traceback
#import signal
#import time
#import locale
#import sys
#sys.setdefaultencoding('utf-8')

#HOST = '127.0.0.1'
#PORT = 8000

root_path = ""
#testof = ""
root_path = os.path.abspath(os.path.split(__file__)[0])
#os.environ['LANG']='ru_RU.UTF-8'
#os.environ['LC_ALL']='ru_RU.UTF-8'
#os.environ['LC_LANG']='ru_RU.UTF-8'
#os.environ['LC_CTYPE']='ru_RU.UTF-8'
#os.environ['CTYPE']='ru_RU.UTF-8'
#os.environ['PYTHONIOENCODING']='utf8'
#os.environ["PYTHONIOENCODING"] = "utf-8"
#scriptLocale=locale.setlocale(category=locale.LC_ALL, locale="ru_RU.UTF-8")
#os.environ['FS_ENCODING']='utf8'
#os.environ['fs_encoding']='utf8'
#os.environ['LC_CTYPE']='en_US.UTF-8'
#os.environ['LC_NUMERIC']='en_US.UTF-8'
#os.environ['LC_TIME']='en_US.UTF-8'
#os.environ['LC_COLLATE']='en_US.UTF-8'
#os.environ['LC_MONETARY']='en_US.UTF-8'
#os.environ['LC_MESSAGES']='en_US.UTF-8'
#os.environ['LC_PAPER']='en_US.UTF-8'
#os.environ['LC_NAME']='en_US.UTF-8'
#os.environ['LC_ADDRESS']='en_US.UTF-8'
#os.environ['LC_TELEPHONE']='en_US.UTF-8'
#os.environ['LC_MEASUREMENT']='en_US.UTF-8'
#os.environ['LC_IDENTIFICATION']='en_US.UTF-8'


f = open(os.path.join(root_path, 'wsgi.log'), 'a')

#def application(environ, start_response):
#    if environ['mod_wsgi.process_group'] != '': 
#        import signal
#        os.kill(os.getpid(), signal.SIGINT)
#    return ["killed"]
try:
    sys.path.insert(0, os.path.join(root_path, 'venv/lib/python3.6/site-packages/')) if not ((os.path.join(root_path, 'venv/lib/python3.6/site-packages/')) in str(sys.path)) else '', 
#    sys.path.insert(0, os.path.join(root_path, 'venv/src/google-analytics/')) if not ((os.path.join(root_path, 'venv/src/google-analytics/')) in str(sys.path)) else '',
#    sys.path.insert(0, os.path.join(root_path, 'venv/src/sociallinks/')) if not ((os.path.join(root_path, 'venv/src/sociallinks/')) in str(sys.path)) else '',
#    sys.path.insert(0, os.path.join(root_path, 'venv/src/news/')) if not ((os.path.join(root_path, 'venv/src/news/')) in str(sys.path)) else '',
    sys.path.insert(0, os.path.join(root_path, 'eifmanacademy/')) if not ((os.path.join(root_path, 'eifmanacademy/')) in str(sys.path)) else '',

    os.environ['SECRET_KEY'] = 'django-insecure-x$0*(5+w@lmc__8x^=^n2mn2a%6w2%998=)4)13v!!&6&7dop7'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'eifmanacademy.settings'



    import django
#    f.write(django.get_version())
#    f.write('\n\n')
#    f.write(str(sys.path))
    django.setup()
#    from django.core.wsgi import get_wsgi_application
#    application = get_wsgi_application()
    from django.core.handlers import wsgi
    application = wsgi.WSGIHandler()
#    application = django.core.handlers.wsgi.WSGIHandler()
    
except Exception as excep:
    f.write(django.get_version())
    f.write('\n\n')
    f.write(str(sys.path))

#    if 'mod_wsgi' in sys.modules:
#    exceptmy = traceback.print_exc()
#        os.kill(os.getpid(), signal.SIGINT)
#        time.sleep(2.5)
#    f.write("%s %s" % (datetime.now(), exceptmy))
#    f.write('\n\n')
#    f.write(application)
#    from django.core.wsgi import get_wsgi_application
#    application = "eifmanacademy"
    f.write("Not Loaded at {}\n".format(datetime.now()))
#    f.write('\n\n')
#    f.write(exceptmy)
#    f.writex(excep)
#import sys
#sys.stdout = sys.stderr
#f.write(os.environ['wsgi.errors'])
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
#from eifmanacademy.wsgi import application
#import locale
#f.write(str(locale.getlocale()))
f.write('\n\n')
f.write('\n\n')
f.write(str(sys.path))
f.write("Loaded at {}\n".format(datetime.now()))
#exceptmy = 'empty'
#exceptmy = traceback.print_exec()
#f.write(exceptmy)
f.close()
#import django
#django.setup()

#from django.core.handlers import wsgi
#application = wsgi.WSGIHandler()
#application = django.core.handlers.wsgi.WSGIHandler()