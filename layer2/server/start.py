#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()
from socketio.server import SocketIOServer

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","server.settings")

from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(application)

if __name__ == '__main__':
	HOST = getattr(settings,'WSGI_HOSTNAME','0.0.0.0')
	PORT = getattr(settings,'WSGI_PORT',8000)
	print "Starting server on http://%s:%d" % (HOST, PORT)
	server = SocketIOServer((HOST,PORT), application)
	server.serve_forever()
