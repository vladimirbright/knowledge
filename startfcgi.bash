#!/bin/bash

PIDFILE='/var/run/knowledge.pid'
SOCKETFILE='/tmp/knowledge.sock'
HOST='127.0.0.1'
PORT=5757
ERRLOG='/var/log/knowledge.fastcgi.error.log'

if [ -f $PIDFILE ]; then
    kill `cat  "$PIDFILE"`
    rm -f  "$PIDFILE"
fi


python manage.py runfcgi     \
host=$HOST              \
port=$PORT              \
pidfile=$PIDFILE        \
#socket=$SOCKETFILE      \
maxrequests=1000        \
maxspare=50             \
minspare=5              \
errlog=$ERRLOG

