#!/bin/sh

wget http://192.168.1.97:31338/scanner 

while [ ! -f scanner ]; do
    sleep 1
done

wget http://192.168.1.97:31338/loader

while [ ! -f loader ]; do
    sleep 1
done


chmod +x scanner
chmod +x loader