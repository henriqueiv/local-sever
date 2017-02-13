#!/bin/bash

if (( $(ps -aux | grep -v grep | grep "420bits-service.py" | wc -l) > 0 ))
then
echo "420bits-service.py is already running"
else
echo "Will start 420bits-service.py"
/usr/bin/python "/home/pi/420bits/local-sever/420bits-service.py" > "/home/pi/420bits/logs/420bits-service.log" 2>&1 &
echo "Did start 420bits-service.py"
fi

if (( $(ps -aux | grep -v grep | grep "420bits-webserver.py" | wc -l) > 0 ))
then
echo "420bits-webserver is running"
else
echo "Will start 420bits-service.py"
/usr/bin/python "/home/pi/420bits/local-sever/420bits-webserver.py" > "/home/pi/420bits/logs/420bits-webserver.log" 2>&1 &
echo "Did start 420bits-webserver.py"
fi