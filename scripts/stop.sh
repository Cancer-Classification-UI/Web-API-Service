#!/bin/bash
echo "Killing and removing container..."
docker kill web-api
docker rm web-api
echo "Container stopped"
