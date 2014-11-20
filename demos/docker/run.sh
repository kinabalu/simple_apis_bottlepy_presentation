#!/bin/bash

case "$1" in
    # db, flup, web run the containers with the expected settings
    mongo)
        docker run -d --name mongo -p 27017:27017 wine/mongo
        ;;
    flup)
        docker run -d --name flup --link mongo:mongo wine/flup
        ;;
    web)
        docker run -d --name web -p 80:80 --link mongo:mongo --link flup:flup wine/web
        ;;
    *)
        exit 1
esac