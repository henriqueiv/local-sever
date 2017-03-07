from tornado import web
import json
from app.apihandlers.accessorylogapihandler import AccessoryLogAPIHandler
from app.factories.accessorylogfactory import AccessoryLogFactoryGetParams

class AccessoryLogsRequestHandler(web.RequestHandler):

    accessory_log_api_handler = AccessoryLogAPIHandler()

    @web.asynchronous
    def get(self, *args):
        params = AccessoryLogFactoryGetParams()
        params.from_date = self.get_query_argument("from_date", None)
        params.to_date = self.get_query_argument("to_date", None)
        params.accessory_id = self.get_query_argument("accessory_id", None)
        params.limit = int(self.get_query_argument("limit", 0))
        
        json = self.accessory_log_api_handler.get_as_json_string(params)

        self.write(json)
        self.finish()