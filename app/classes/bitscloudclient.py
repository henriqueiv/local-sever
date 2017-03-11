import time
import websocket as _websocket
import threading
import thread

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
        remote_ws = _websocket.WebSocketApp("ws://127.0.0.1:8890/ws",
                      on_message = self.on_message_remote,
                      on_error = self.on_error_remote,
                      on_close = self.on_close_remote)
        remote_ws.on_open = self.on_open_remote

        def retry():
            if remote_ws is not None:
                try:
                    remote_ws.run_forever()
                except Exception as e:
                    print "Error: " + str(e)

        wst_remote = threading.Thread(target=retry)
        wst_remote.daemon = True
        wst_remote.start()

    def on_message_remote(self, ws, message):
        try:
            if self.on_message is not None:
                self.on_message(message, ws)
        except Exception, e:
            print "error: " + str(e)

    def on_error_remote(self, ws, error):
        def delay_and_retry():
            time.sleep(self.reconnect_timeout)
            self.reconnect()
        
        if self.runs_forever:
            a = threading.Thread(target=delay_and_retry)
            a.daemon = True
            a.start()

    def on_close_remote(self, ws):
        if self.on_close is not None:
            self.on_close(ws)

    def on_open_remote(self, ws):
        
        def run(*args):
            ws.send("{\"register\": \"aaa\"}")

        thread.start_new_thread(run, ())

        if self.on_open is not None:
            self.on_open(ws)