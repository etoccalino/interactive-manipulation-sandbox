"""
Monitoring a connection involves a constant, albeit light, traffic between
client and server. This traffic takes the form of packets sent from client to
server, and bounced right back.

The current implementation strives to move as much logic to client code,
keeping the server light and simple. The server logic is trapped in a class to
be mixed in to a BaseNamespace descendant.

The anatomy of a health check packet is as follows:

{
    latency: (number) approximate client lantency in milliseconds.
    timestamp: (number) milliseconds since epoch; used by client.
}
"""


class HealthMonitorMixin(object):
    """
    A mixin for the socketio.namespace.BaseNamespace.

    Allow for "health check" data to bounce back to clients, and retrieve
    connection data in the process to expose to server code.

    The mixed class can define a method "latency_update", which should take a
    single numeric argument, to process new values of connection latency
    reported by the client.
    """

    def on_health_check(self, healthcheck_packet):
        """Acknowledge the health check.

        Returning an iterable, send back the parameters to be passed to the
        acknowledge callback in the client.
        """
        prev_latency = self._connection_latency
        latency = healthcheck_packet['latency']
        if prev_latency != latency:
            # Update latency value for the server.
            self._connection_latency = latency

            # Call back to process the new latency value.
            if hasattr(self, 'latency_update'):
                self.latency_update(latency)

        return [healthcheck_packet['timestamp']]
