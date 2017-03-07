from app.factories.accessorylogfactory import AccessoryLogFactory, AccessoryLogFactoryGetParams
import json

DefaultMaxLimit = 1000

class AccessoryLogAPIHandler:
    
    log_factory = AccessoryLogFactory()

    def get_as_objects(self, get_params = AccessoryLogFactoryGetParams()):
        if get_params.limit is not None:
            get_params.limit = DefaultMaxLimit if get_params.limit == 0 else min(get_params.limit,DefaultMaxLimit)

        try:
        	logs = self.log_factory.get_logs_for_api(get_params)
        	return logs
        except Exception as e:
        	return {"errors": [{"message": str(e)}]}

    def get_as_json_string(self, get_params = AccessoryLogFactoryGetParams()):
        return json.dumps(self.get_as_objects(get_params))