import time
import websocket as _websocket
import threading
import thread
from app.configs import BitsCloudClientConfig

class BitsCloudClient:
    
    debug = False
    reconnect_timeout = 2
    runs_forever = False

    on_close = None
    on_open = None
    on_message = None

    def run_forever(self):
        self.runs_forever = True
        self.reconnect()

    def reconnect(self):
        _websocket.enableTrace(self.debug)
        remote_ws = _websocket.WebSocketApp(BitsCloudClientConfig.server_address,
                      on_message = self.received_message_from_cloud,
                      on_error = self.cloud_connection_error,
                      on_close = self.cloud_connection_close)
        remote_ws.on_open = self.cloud_connection_open

        def retry():
            if remote_ws is not None:
                try:
                    remote_ws.run_forever()
                except Exception as e:
                    print "Error: " + str(e)

        wst_remote = threading.Thread(target=retry)
        wst_remote.daemon = True
        wst_remote.start()

    def received_message_from_cloud(self, ws, message):
        try:
            if self.on_message is not None:
                self.on_message(message, ws)
        except Exception, e:
            print "error: " + str(e)

    def cloud_connection_error(self, ws, error):
        def delay_and_retry():
            time.sleep(self.reconnect_timeout)
            self.reconnect()
        
        if self.runs_forever:
            a = threading.Thread(target=delay_and_retry)
            a.daemon = True
            a.start()

    def cloud_connection_close(self, ws):
        if self.on_close is not None:
            self.on_close(ws)

    def cloud_connection_open(self, ws):
        def run(*args):
            ws.send("{\"register\": \"" + BitsCloudClientConfig.device_identifier + "\"}")

        thread.start_new_thread(run, ())

        if self.on_open is not None:
            self.on_open(ws)