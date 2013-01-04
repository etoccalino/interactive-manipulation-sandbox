'''
This django view is only used to link request to gevent-socketio namespaces
'''
from socketio import socketio_manage
from socketio.virtsocket import Socket
from namespace import ClientNamespace
from health_monitor import HealthMonitor


def socketio(request):
        socketio_manage(request.environ, {
                        Socket.GLOBAL_NS: HealthMonitor,
                        '/client': ClientNamespace,
                        }, request)
