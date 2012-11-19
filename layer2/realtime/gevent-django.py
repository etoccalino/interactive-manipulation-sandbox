#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()
from gevent.wsgi import WSGIServer

import sys; sys.path.append("../server")
from server import settings
from django.core.management import setup_environ    
setup_environ(settings)

PORT = 9090

from django.core.handlers.wsgi import WSGIHandler as DjangoWSGIApp
application = DjangoWSGIApp()

if __name__ == '__main__':
    print "Starting server on http://0.0.0.0:%d" % PORT
    server = WSGIServer(("0.0.0.0", PORT), application)
    server.serve_forever()
