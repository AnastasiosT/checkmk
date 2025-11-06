#!/bin/bash

#1. create a bash file with the following name
#2. make it executable with chmod +x licensecount.sh
#3. run it as root like this: su - SITENAME -c '/tmp/licensecount.sh


H=$(lq "GET hosts\nStats: state ~ *")
S=$(lq "GET services\nStats: state ~ *")

echo "Services: $S Hosts: $H"
