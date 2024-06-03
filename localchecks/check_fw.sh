#!/bin/bash

# Get the firewall service details
FW_STATUS=$(systemctl is-active firewalld)
FW_NAME=$(systemctl show -p Description firewalld | cut -d'=' -f2)
date=$(date +%s)

# Define the filename for the output
FILENAME="/var/lib/check_mk_agent/spool/300_check_fw.txt"

# Check if the firewall service is running
if [ "$FW_STATUS" == "active" ]; then
    #echo "0 Firewall - $FW_NAME $FW_STATUS"
    CONTENT="<<<local:cached($date,300)>>>
0 Firewall - $FW_NAME $FW_STATUS
"
else
    #echo "2 Firewall - $FW_NAME $FW_STATUS"
    CONTENT="<<<local:cached($date,300)>>>
2 Firewall - $FW_NAME $FW_STATUS
"
fi

# Prepend a newline to ensure the file starts with a new line
CONTENT="$CONTENT"

# Write the firewall status to the file
echo -e "$CONTENT" > "$FILENAME"

