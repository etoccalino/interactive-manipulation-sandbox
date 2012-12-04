from socketio.namespace import BaseNamespace
import redis
import json

# TODO: See proper place to initilize and maintain connection to redis
redis = redis.Redis('localhost')

class ClientNamespace(BaseNamespace):

#    def __init__(self, *args, **kwArgs):
#        super(ClientNamespace, self).__init__(*args,**kwArgs)

    '''Called by the client to indicate the user has navigated to another
       page or context within the client application'''
    def on_context_new(self, new_context):
        # In order to implement this, we use a key store with:
        # - HASH context: set of users in this context. Each user entry contains: userid and names
        # Information to the client will go by registering to updates in the 'context' key
        print "(socket) New context: %s" % new_context

        # Get the session key, which will identify this particular client
        # TODO: This should probably be done on a more general connect event and kept
        # around throughout this user's session
        session = self.request.session
        if session.session_key is None:
            session.save()
        print "(socket) Session Key = %s" % session.session_key
        self.session_key = session.session_key

        old_context = getattr(self,'context',None)
        self.context = new_context

        # Delete and notify old context if there is one
        if old_context:
            redis.hdel('context:%s' % old_context, self.session_key)
            self.update_contexts( old_context)

        # Update and notify new value
        redis.hset('context:%s' % new_context, self.session_key, make_user_json)
        self.update_contexts( new_context)

    '''Send a message to all the connected clients which are in the context being updated'''
    def update_contexts( self, context):
        clients = redis.hgetall('context:%s' % context)
        for sessid, socket in self.socket.server.sockets.iteritems():
            print "sessid: %s" % sessid
            if socket.context == context:
                socket.emit('context_others', clients)
        
def make_user_json( user):
    if user.username == '':
        return {
            'username': 'AnonymousUser',
            'first_name': '',
            'last_name': 'Anonymous'
        }
    else:
        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }

