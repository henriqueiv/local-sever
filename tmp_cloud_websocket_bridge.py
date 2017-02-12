import websocket
import thread
import time

remote_ws = None
local_ws = None

def on_message_remote(ws, message):
	local_ws.write(message)
	print message
def on_error_remote(ws, error):
    print error
def on_close_remote(ws):
    print "### closed remote ###"
def on_open_remote(ws):
    def run(*args):
    	ws.send("{\"register\": \"aaa\"}")
    thread.start_new_thread(run, ())
def on_message_local(ws, message):
	remote_ws.write(message)
    print message
def on_error_local(ws, error):
    print error

def on_close_local(ws):
    print "### closed local ###"

def on_open_local(ws):
	print "### opened local ###"

websocket.enableTrace(True)

remote_ws = websocket.WebSocketApp("ws://ec2-52-34-138-21.us-west-2.compute.amazonaws.com:8888/websocket",
                          on_message = on_message_remote,
                          on_error = on_error_remote,
                          on_close = on_close_remote)
remote_ws.on_open = on_open_remote
remote_ws.run_forever()


local_ws = websocket.WebSocketApp("ws://127.0.0.1:8888/ws",
                          on_message = on_message_local,
                          on_error = on_error_local,
                          on_close = on_close_local)
local_ws.on_open = on_open_local
local_ws.run_forever()