#!/bin/bash
# startServer.sh - Sam Lovering - 5/12/24
# This script starts the flask and npm servers.
# Todo:
# Investigate putting servers into tmux instance
# Make startup script production friendly
# add proper logging


start_flask_server() {
    echo "Starting Flask server..."
    source ~/55ATAT/venv/bin/activate
    cd ~/55ATAT/flaskServer
    flask run
}

start_npm_server() {
    echo "Starting NodeJS Server in Development Mode."
    cd ~/55ATAT/client
    (npm run dev&)
}

start_flask_server &
start_npm_server
