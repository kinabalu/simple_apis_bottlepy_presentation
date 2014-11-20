#!/bin/bash

case "$1" in
    # Build all the containers and get ready for images to be run
    all)
        docker build -t mystic/baseimage .
        cd web
        docker build -t wine/web .
        cd ../flup
        docker build -t wine/flup .
        cd ../mongo
        docker build -t wine/mongo .
        ;;
    base)
        docker build -t mystic/baseimage .
        ;;
    web)
        cd web
        docker build -t wine/web .
        ;;
    flup)
        cd flup
        docker build -t wine/flup .
        ;;
    mongo)
        cd mongo
        docker build -t wine/mongo .
        ;;
    *)
        exit 1
esac