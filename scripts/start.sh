#!/bin/bash
cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"
echo "Starting container..."
echo "Clearing log file..."
> $SCRIPT_DIR/../log.txt
echo "Running image..."
docker run -d -e GRADIO_SERVER_NAME=0.0.0.0 -e PYTHONUNBUFFERED=1 $(
if [ -f "$SCRIPT_DIR/../.env" ]; then
    grep -oP 'APP_PORT=\K\d+' $SCRIPT_DIR/../.env | awk '{ print "-p "$1":"$1 }'
else
    echo "-p 8080:8080"
fi
) -v $SCRIPT_DIR/../log.txt:/usr/src/app/log.txt --name web-api ccu-web-api
echo "Container started"