#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()
from socketio.server import SocketIOServer

import sys; sys.path.append("../server")
from server import settings
from django.core.management import setup_environ
setup_environ(settings)

PORT = 8000

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, "apps"))

if __name__ == '__main__':
	print "Listening on http://127.0.0.1:%s and on port 10843 (flash policy server)" % PORT
	SocketIOServer(('', PORT), application, resource="socket.io").serve_forever()
