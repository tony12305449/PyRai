#!/bin/sh

curl http://192.168.1.97:31338/scanner -o scanner

while [ ! -f scanner ]; do
    sleep 1
done

curl http://192.168.1.97:31338/loader -o loader

while [ ! -f loader ]; do
    sleep 1
done


chmod +x scanner
chmod +x loader