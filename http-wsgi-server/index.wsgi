import os
import time
import sys
cdir = os.path.dirname(__file__)
sys.path.append('./xml')
#from xml import xmlprocessor
if cdir not in sys.path:
    sys.path.append(cdir)
    os.chdir(cdir)
    os.environ['PYTHON_PATH'] = cdir 
#sys.path.append('/var/www/django/xmlprocessor')
#sys.path.insert(0, '/var/www/django/xmlprocessor')
#print sys.path
#import xmlprocessor
activate_this = '/home/krozin/pywsgi/server/xml/xmlprocessor.py'
execfile(activate_this, dict(__file__=activate_this))
import xmlprocessor


def application(environ, start_response):
    status = '200 OK'
    output = str(time.time()) # + str(environ)
    response_headers = [('Content-type', 'text/plain'),
                    ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    print cdir
    print sys.path
    print xmlprocessor.test()
    return [output]

def api():
    pass

"""
curl http://localhost/django/api.wsgi -d "<?xml version='1.0' encoding='utf-8'?><request><requestType g='sss' k='bbb'>NBI_ISMS_MDN_VERIFICATION_REQUEST</requestType></request>"
"""
application = application

