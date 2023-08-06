"""WebSocket-specific events."""
from eavesdropper.pkg_data.mitmproxy import http
from eavesdropper.pkg_data.mitmproxy import websocket
from . import GenericEvents


class Events(GenericEvents):
    # Websocket lifecycle
    def websocket_handshake(self, flow: http.HTTPFlow):
        """
            Called when a client wants to establish a WebSocket connection. The
            WebSocket-specific headers can be manipulated to alter the
            handshake. The flow object is guaranteed to have a non-None request
            attribute.
        """

    def websocket_start(self, flow: websocket.WebSocketFlow):
        """
            A websocket connection has commenced.
        """

    def websocket_message(self, flow: websocket.WebSocketFlow):
        """
            Called when a WebSocket message is received from the client or
            server. The most recent message will be flow.messages[-1]. The
            message is user-modifiable. Currently there are two types of
            messages, corresponding to the BINARY and TEXT frame types.
        """

    def websocket_error(self, flow: websocket.WebSocketFlow):
        """
            A websocket connection has had an error.
        """

    def websocket_end(self, flow: websocket.WebSocketFlow):
        """
            A websocket connection has ended.
        """
