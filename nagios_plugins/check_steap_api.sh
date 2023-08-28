#!/bin/bash

IP=""
KEY=""
USAGE="

$0 [-h ] [-i]  
   -i IP
   -k KEY
   -h HELP
"


while getopts k:i:h: option; do
    case "${option}" in
        i) IP=${OPTARG}
            ;;
	k) KEY=${OPTARG}
		;;
        h|*)echo "$USAGE"
            exit 0
            ;;
    esac
done

echo $IP
echo $KEY


RESP=$(curl -G -s -d filter=\addr\\$IP \
	https://api.steampowered.com/IGameServersService/GetServerList/v1/?key=$KEY&limit=50 |jq -c '.[] | .servers')

echo $RESP

if [ -z "$RESP" ] 
then 
	echo "CRIT - TEST HHHHH"
	exit 2
else 
	echo "OK - TEST HHHHH"
	exit 0


fi
