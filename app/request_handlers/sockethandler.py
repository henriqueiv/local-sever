from app.apihandlers.socketapihandler import SocketAPIHandler
from tornado import websocket, web, ioloop

class SocketHandler(websocket.WebSocketHandler):

    on_close_callback = None
    on_open_callback = None
    on_message_callback = None

    def initialize(self, on_close, on_message, on_open):
        self.on_close_callback = on_close
        self.on_message_callback = on_message
        self.on_open_callback = on_open
        print "initialize"

    def check_origin(self, origin):
        return True

    def open(self):
        if self.on_open_callback is not None:
            self.on_open_callback(self)

    def on_close(self):
        if self.on_close_callback is not None:
            self.on_close_callback(self)

    def on_message(self, message):
        if self.on_message_callback is not None:
            self.on_message_callback(message, self)