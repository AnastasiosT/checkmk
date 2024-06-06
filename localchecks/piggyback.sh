#!/bin/bash

echo "<<<<___ATL___PIGGY1___ATL___>>>>"
echo "<<<local:cached($(date +%s),300)>>>"
echo "0 \"IMC Status\" - No Alarm"
echo "<<<labels:sep(0)>>>"
echo '{"abc/host": "yes"}'
echo '{"mrwitmann/host": "whazup"}'
echo "<<<<>>>>"
echo "<<<<___ATL___PIGGY2___ATL___>>>>"
echo "<<<local:cached($(date +%s),300)>>>"
echo "0 dummy - Find news https://www.google.de/search?q=checkmk&tbm=nws about checkmk."
echo "<<<labels:sep(0)>>>"
echo '{"abc/host": "yes"}'
echo '{"mrwitmann/host": "whazup"}'
echo '<<<<>>>>'
echo "<<<<___ATL___PIGGY3___ATL___>>>>"
echo "<<<labels:sep(0)>>>"
echo '{"abc/host": "yes"}'
echo '{"mrwitmann/host": "whazup"}'
echo '<<<<>>>>'
