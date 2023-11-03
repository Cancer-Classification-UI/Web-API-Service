#!/bin/bash
cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"
echo "Starting container..."
echo "Running image..."
docker run -d -e GRADIO_SERVER_NAME=0.0.0.0 -e PYTHONUNBUFFERED=1 $(
if [ -f "$SCRIPT_DIR/../.env" ]; then
    grep -oP 'APP_PORT=\K\d+' $SCRIPT_DIR/../.env | awk '{ print "-p "$1":"$1 }'
else
    echo "-p 8082:8082"
fi
) --name web-api ccu-web-api
echo "Container started"