import smbus
import time

def StringToBytes(val):
  retVal = []
  for c in val:
    retVal.append(ord(c))
  return retVal

def readBus():
  data = ""
  for i in range(0, 1):
          data += chr(bus.read_byte(address));
  print data


bus = smbus.SMBus(1)
address = 0x04

#bus.write_i2c_block_data(address, 0, StringToBytes("Hello World"))

while True:
	bytes = bus.read_i2c_block_data(address, 0)
	print "".join(map(chr, bytes)).strip("\xff")
	time.sleep(1)