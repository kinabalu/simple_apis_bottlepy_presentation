#!/bin/sh

sed -i "s/%flup-ip%/$FLUP_PORT_8000_TCP_ADDR/" /etc/nginx/sites-available/default

exec /usr/sbin/nginx