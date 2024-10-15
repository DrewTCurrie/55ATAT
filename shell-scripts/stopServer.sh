#!/bin/bash

# stopServer.sh Sam Lovering 5/12/24
# This program stops the npm and flask server
# TODO:
# This is probably an unsafe way to stop these processes.

echo "Stopping Servers"
pkill -SIGINT -f vite.js
pkill -SIGINT -f flask
tset
