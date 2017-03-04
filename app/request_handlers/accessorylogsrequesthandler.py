from tornado import web
from app.factories.accessorylogfactory import AccessoryLogFactory, AccessoryLogFactoryGetParams
import json

DefaultMaxLimit = 1000

class AccessoryLogsRequestHandler(web.RequestHandler):

    log_factory = AccessoryLogFactory()

    @web.asynchronous
    def get(self, *args):
        limit = min(int(self.get_query_argument("limit", DefaultMaxLimit)),DefaultMaxLimit)
        if limit == 0:
            limit = DefaultMaxLimit

        params = AccessoryLogFactoryGetParams()
        params.start_timestamp = self.get_query_argument("start_timestamp", None)
        params.end_timestamp = self.get_query_argument("end_timestamp", None)
        params.accessory_id = self.get_query_argument("accessory_id", None)
        params.limit = limit
        
        self.write(json.dumps(self.log_factory.get_logs_for_api(params)))
        
        self.finish()
        print "AccessoriesHandler Received get request."