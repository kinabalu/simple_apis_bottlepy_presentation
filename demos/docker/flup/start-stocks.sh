#!/bin/sh

cd /var/www

/usr/bin/python /var/www/app.py --host 0.0.0.0 -p 8000 --mongo-host mongo --fcgi