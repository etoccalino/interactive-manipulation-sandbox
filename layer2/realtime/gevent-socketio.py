#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio import socketio_manage

PORT = 9090

class MyNamespace(BaseNamespace):
    def on_jac_event(self, msg):
        print "on_jac_event: %s" % msg

class MyWSGIApp:
    def __call__(self, environ, start_response):
        socketio_manage(environ, {'/jac_ns': MyNamespace})
        
if __name__ == '__main__':
    print "Listening on http://127.0.0.1:%s and on port 10843 (flash policy server)" % PORT
    SocketIOServer(('', PORT), MyWSGIApp(), resource="socket.io").serve_forever()
