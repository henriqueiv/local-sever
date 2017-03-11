from tornado import web
import json
from app.apihandlers.accessorylogapihandler import AccessoryLogAPIHandler
from app.factories.accessorylogfactory import AccessoryLogFactoryGetParams

class AccessoryLogsRequestHandler(web.RequestHandler):

    accessory_log_api_handler = AccessoryLogAPIHandler()

    @web.asynchronous
    def get(self, *args):
        params = AccessoryLogFactoryGetParams()
        params.from_date = self.get_query_argument(AccessoryAPIHandler.Constants.FromDateParam, None)
        params.to_date = self.get_query_argument(AccessoryAPIHandler.Constants.ToDateParam, None)
        params.accessory_id = self.get_query_argument(AccessoryAPIHandler.Constants.AccessoryIDParam, None)
        params.limit = int(self.get_query_argument(AccessoryAPIHandler.Constants.LimitParam, 0))
        
        json = self.accessory_log_api_handler.get_as_json_string(params)

        self.write(json)
        self.finish()