import json

class SocketMessageURI:

    action = None
    topic = None
    uri = None

    class Constants:
        URIActionIndex = 0
        URITopicIndex = 1

        URIGetAction = "get"
        URIPostAction = "post"
        URIDeleteAction = "delete"

    def __init__(self, raw_string_uri):
        self.uri = raw_string_uri
        self.parse_uri()

    def parse_uri(self):
        self.action = self.action_for_current_uri()
        self.topic = self.topic_for_current_uri()

    def action_for_current_uri(self):
        return self.uri_items(self.uri, SocketMessageURI.Constants.URIActionIndex)

    def topic_for_current_uri(self):
        return self.uri_items(self.uri, SocketMessageURI.Constants.URITopicIndex)

    def uri_items(self, uri, index = None):
        if uri is None:
            return None

        parts = uri.split("/")
        if index is None:
            return parts
        elif len(parts) - 1 >= index:
            return parts[index]

        return None

    def has_topic(self):
        return self.topic is not None

    def is_get_action(self):
        return self.action == SocketMessageURI.Constants.URIGetAction

    def is_post_action(self):
        return self.action == SocketMessageURI.Constants.URIPostAction

    def is_delete_action(self):
        return self.action == SocketMessageURI.Constants.URIDeleteAction

class SocketMessage:

    id = None
    token = None
    arguments = None
    object = None
    raw_message = None
    uri = None

    class Constants:
        IDKey = "_id"
        URIKey = "uri"
        TokenKey = "token"
        ArgumentsKey = "arguments"
        ObjectKey = "object"


    def __init__(self, socket_message):
        try:
            self.raw_message = socket_message
            message_object = json.loads(self.raw_message)

            if message_object.has_key(SocketMessage.Constants.URIKey):
                self.uri = SocketMessageURI(message_object[SocketMessage.Constants.URIKey])

            if message_object.has_key(SocketMessage.Constants.IDKey):
                self.id = message_object[SocketMessage.Constants.IDKey]

            if message_object.has_key(SocketMessage.Constants.TokenKey):
                self.token = message_object[SocketMessage.Constants.TokenKey]

            if message_object.has_key(SocketMessage.Constants.ArgumentsKey):
                self.arguments = message_object[SocketMessage.Constants.ArgumentsKey]

            if message_object.has_key(SocketMessage.Constants.ObjectKey):
                self.object = message_object[SocketMessage.Constants.ObjectKey]

        except Exception as e:
            print("error parsing message:" + str(e))

    def argument(self, name, default_value = None):
        if self.arguments is not None and self.arguments.has_key(name):
            return self.arguments[name]
        return default_value