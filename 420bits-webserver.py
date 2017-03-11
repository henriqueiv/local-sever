
import os
from tornado import web, ioloop

from app.models.appapi import AppAPI
from app.apihandlers.socketapihandler import SocketAPIHandler
from app.classes.socketclientsupdater import SocketClientsUpdater
from app.classes.bitscloudclient import BitsCloudClient
from app.request_handlers.accessorylogsrequesthandler import AccessoryLogsRequestHandler
from app.request_handlers.tasksrequesthandler import TasksRequestHandler
from app.request_handlers.updateclientshandler import UpdateClientsHandler
from app.request_handlers.notesrequesthandler import NotesRequestHandler
from app.request_handlers.accessoryrequesthandler import AccessoryRequestHandler
from app.request_handlers.userrequesthandler import UserRequestHandler
from app.request_handlers.sockethandler import SocketHandler


clients_updater = SocketClientsUpdater()

socket_api_handler = SocketAPIHandler()
cloud_client = BitsCloudClient()

socket_api_handler.on_read = clients_updater.update_client
socket_api_handler.on_update = clients_updater.update_all_clients

cloud_client.on_open = clients_updater.add_client
cloud_client.on_close = clients_updater.remove_client
cloud_client.on_message = socket_api_handler.dispatch

socket_handler_params =  {"on_close": clients_updater.remove_client, "on_message": socket_api_handler.dispatch, "on_open": clients_updater.add_client}
app = web.Application([
    (r'/ws', SocketHandler, socket_handler_params),
    (r'/' + AppAPI.Constants.UsersTopic, UserRequestHandler),
    (r'/' + AppAPI.Constants.TasksTopic, TasksRequestHandler,dict(clients_updater = clients_updater)),
    (r'/' + AppAPI.Constants.NotesTopic, NotesRequestHandler,dict(clients_updater = clients_updater)),
    (r'/' + AppAPI.Constants.AccessoriesLogsTopic, AccessoryLogsRequestHandler),
    (r'/' + AppAPI.Constants.AccessoriesTopic, AccessoryRequestHandler),
    (r'/update_clients', UpdateClientsHandler, dict(clients_updater = clients_updater)),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])


if __name__ == '__main__':
    cloud_client.run_forever()
    app.listen(8888)
    ioloop.IOLoop.instance().start()
