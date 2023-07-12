#!/bin/bash

if [ -z "$1" ]; then
    if [ -z "${DUCKDNSTOKEN}" ]; then
        echo "DUCKDNSTOKEN not set. Pass as first parameter or set it as environement var."
        exit 1
    fi
else
    DUCKDNSTOKEN=$1
fi

current_dir="$(dirname "$(realpath "$0")")"
config_dir="$current_dir/swag_config"

# if [ ! "$(docker network ls | grep hri_net)" ]; then
#   echo "Creating hri_net network ..."
#   docker network create hri_net
# else
#   echo "hri_net network exists"
# fi


docker run -d\
  --name=hri_swag \
  --cap-add=NET_ADMIN \
  --net=host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/London \
  -e URL=hriproject.duckdns.org \
  -e SUBDOMAINS=www,websocket, \
  -e VALIDATION=http \
  -e DUCKDNSTOKEN="$DUCKDNSTOKEN" \
  -v "$config_dir":/config \
  --restart unless-stopped \
  lscr.io/linuxserver/swag