#!/bin/bash
# Restart nullmailer Service


nullmailer_state=`systemctl status nullmailer |grep Active|awk -F ' ' '{print $2}'`
date=`date +"%Y-%m-%d %H:%M:%S"`

if [[ $nullmailer_state == "inactive" ]]
then
	echo "restarting nullmailer service"
	systemctl restart nullmailer
        journalctl -u nullmailer --since "$date" &>/tmp/alert_output_$(date +%s)

else 
	echo "the service is already running. No need to restart it"
fi



