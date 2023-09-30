#!/bin/bash
cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"
echo "Starting container..."
echo "Clearing log file..."
> $SCRIPT_DIR/../log.txt
echo "Running image..."
docker run -d -e GRADIO_SERVER_NAME=0.0.0.0 -p $(cat $SCRIPT_DIR/../.env | grep APP_PORT | cut -d= -f2 | awk '/^/ { print $1":"$1 }') -v $SCRIPT_DIR/../log.txt:/usr/src/app/log.txt --name web-api ccu-web-api
echo "Container started"