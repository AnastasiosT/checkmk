#!/bin/bash
# Checkmk agent plugin to generate 100 host labels
# Place in: /usr/lib/check_mk_agent/plugins/ (or local/lib/check_mk_agent/plugins/ on the site)

echo "<<<labels:sep(0)>>>"

for i in $(seq 1 100); do
    echo "{\"autolabel_${i}/host\": \"value_${i}\"}"
done
