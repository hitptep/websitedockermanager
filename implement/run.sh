#!/bin/bash


#润
docker run --name $1-$2-$3 -P $1:$2
cd ../communication
#python3 sendPorts.py $1-$2-$3
docker rm $(docker ps -a -q)