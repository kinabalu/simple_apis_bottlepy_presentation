#!/bin/sh

mongoimport -d stocks stocks.json

exec /usr/bin/mongod