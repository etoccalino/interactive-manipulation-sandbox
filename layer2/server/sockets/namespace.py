from socketio.namespace import BaseNamespace

class ClientNamespace(BaseNamespace):
	def on_new_context(self, msg):
		print "New context: %s" % msg
