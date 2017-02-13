#!/bin/bash
420bits_service="~/420bits/local-server/420bits-service.py"

if (( $(ps -ef | grep -v grep | grep $service | wc -l) > 0 ))
then
echo "$service is running!!!"
else
/usr/bin/python ~/420bits/local-server/420bits-service.py > ~/420bits/logs/420bits-service.log 2>&1 &
fi