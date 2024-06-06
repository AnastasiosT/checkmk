#!/bin/bash
cpu_utilization=$(top -bn1 | grep "Cpu(s)" | awk '

{printf "%.2f", $2 + $4}
')

#echo "CPU Utilization: ${cpu_utilization}%"

echo "P \"Custom-Check CPU % Utilization\" Total-CPU=${cpu_utilization}4:;5; CPU% load monitoring with lower and upper thresholds"

echo "P \"Testing lower\" CPU=${cpu_utilization};6:;4: Service with lower threshholds only"
