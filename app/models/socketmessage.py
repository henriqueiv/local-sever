import json


SocketMessageActionRead = "read"
SocketMessageActionTurnOn = "turn_on"
SocketMessageActionTurnOff = "turn_off"

class SocketMessage:

    action = None
    id = None
    token = None
    arguments = None
    object = None
    raw_message = None

    def __init__(self, socket_message):
        try:
            self.raw_message = socket_message
            message_object = json.loads(self.raw_message)

            if message_object.has_key("action"):
                self.action = message_object["action"]

            if message_object.has_key("id"):
                self.id = message_object["id"]

            if message_object.has_key("token"):
                self.token = message_object["token"]

            if message_object.has_key("arguments"):
                self.arguments = message_object["arguments"]

            if message_object.has_key("object"):
                self.object = message_object["object"]

        except:
            print("error parsing message:" + str(socket_message))
            return

    def argument(self, name):
        if self.arguments is not None and self.arguments.has_key(name):
            return self.arguments[name]
        return None