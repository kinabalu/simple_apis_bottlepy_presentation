#!/bin/bash

case "$1" in
    # Build all the containers and get ready for images to be run
    build-all)
        docker build -t mystic/baseimage .
        cd web
        docker build -t wine/web .
        cd ../flup
        docker build -t wine/flup .
        cd ../mongo
        docker build -t wine/mongo .
        ;;
    build-base)
        docker build -t mystic/baseimage .
        ;;
    build-web)
        cd web
        docker build -t wine/web .
        ;;
    build-flup)
        cd flup
        docker build -t wine/flup .
        ;;
    build-mongo)
        cd mongo
        docker build -t wine/mongo .
        ;;
    # Next set of commands db, flup, web run the containers with the expected settings
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