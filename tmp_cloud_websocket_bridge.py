import websocket
import thread
import time

def on_message(ws, message):
    print "Message: " + str(message)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
    	write_a_lot(ws)
        print "thread terminating..."
    thread.start_new_thread(run, ())

def write_a_lot(ws):
	ws.send("{\"register\": \"aaa\"}")
	time.sleep(5)
	write_a_lot(ws)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://ec2-52-34-138-21.us-west-2.compute.amazonaws.com:8888/websocket",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()