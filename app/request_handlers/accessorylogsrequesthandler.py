from tornado import web
from app.factories.accessorylogfactory import AccessoryLogFactory
import json

DefaultMaxLimit = 1000

class AccessoryLogsRequestHandler(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        limit = min(int(self.get_query_argument("limit", DefaultMaxLimit)),DefaultMaxLimit)
        if limit == 0:
            limit = DefaultMaxLimit
        from_timestamp = float(self.get_query_argument("from", 0))

        log_factory = AccessoryLogFactory()
        self.write(json.dumps(log_factory.get_logs_for_api(from_timestamp,limit)))
        
        self.finish()
        print "AccessoriesHandler Received get request."