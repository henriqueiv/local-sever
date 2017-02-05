import app.models
import app.accessory_manager



manager = AccessoryManager()
manager.name = "william"

print manager.name

print manager.get_accessories()