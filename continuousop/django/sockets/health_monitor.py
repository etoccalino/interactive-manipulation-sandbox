"""
Monitoring a connection involves a constant, albeit light, traffic between
client and server. This traffic takes the form of packets sent from client to
server, and bounced right back.

The current implementation strives to move as much logic to client code,
keeping the server light and simple. The server logic is trapped in a class to
be mixed in to a BaseNamespace descendant.
"""


class HealthMonitorMixin(object):
    """
    A mixin for the socketio.namespace.BaseNamespace.

    Allow for "health check" packets to bounce back to clients, and retrieve
    data for them to expose to server code.

    The anatomy of a health check packet is as follows:

    {
        latency: (number) approximate client lantency in milliseconds.
        timestamp: (number) milliseconds since epoch; used by client.
    }
    """

    def on_health_check(self, healthcheck_packet):
        """Acknowledge the health check.

        Returning an iterable, send back the parameters to be passed to the
        acknowledge callback in the client.
        """
        return [healthcheck_packet['timestamp']]
