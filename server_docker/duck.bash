#!/bin/bash

DOMAIN="hriproject"
LOG_FILE="$(dirname $0)/duck.log"
TOKEN="$1"
if [ -z $TOKEN]; then
    echo "Add the duckdns token as parameter"
    exit 1
fi

echo "Updating duckdns ip ..."

echo url="https://www.duckdns.org/update?domains=$DOMAIN&token=$TOKEN" | curl -k -o "$LOG_FILE" -K -