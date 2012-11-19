from socketio import socketio_manage
from namespace import ClientNamespace

def socketio(request):
	socketio_manage(request.environ,{
		'/client': ClientNamespace
	}, request)
	