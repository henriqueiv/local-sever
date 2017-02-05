import models
import smbus
import lib.accessory_manager

AccessoryTypeUndefined = -1
AccessoryTypeHumidity = 0
AccessoryTypeTemperature = 1
AccessoryTypeCO2 = 2

DefaultHumidityAccessoryID = 1
DefaultTemperatureAccessoryID = 2
DefaultCO2AccessoryID = 3



manager = AccessoryManager()
manager.name = "william"

print manager.name

accessory = Accessory("Will","0",AccessoryTypeTemperature)
print accessory.name

print manager.get_accessories()