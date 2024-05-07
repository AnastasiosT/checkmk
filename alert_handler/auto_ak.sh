#!/bin/bash
# Alert Handler der Acknowledge setzt

env |grep ^ALERT_ | sort > $OMD_ROOT/tmp/alert.out

if [ "$ALERT_WHAT" == "SERVICE" ]
then 
        lq "COMMAND [$(date +%s)] ACKNOWLEDGE_SVC_PROBLEM;$ALERT_HOSTNAME;$ALERT_SERVICEDESC;1;2;2;cmkadmin;auto acknoledgement via alert handler"

elif [ "$ALERT_WHAT" == "HOST" ]
then
	lq "COMMAND [$(date +%s)] ACKNOWLEDGE_HOST_PROBLEM;$ALERT_HOSTNAME;1;2;2;cmkadmin;auto acknoledgement via alert handler"

fi

