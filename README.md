# Web API Service
[![Web API Image Deployment](https://github.com/Cancer-Classification-UI/Web-API-Service/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/Cancer-Classification-UI/Web-API-Service/actions/workflows/docker-image.yml)

This service is responsible for the web interface. Interfaces with all backend API's to facilitate interface logic.

This service will most likely not have an API and wont be used. The web interface can be found at

```
http://<ip>:<APP_PORT>
``` 

If you are running locally it would be at [http://127.0.0.1:8082](http://127.0.0.1:8082)

# How to run

## Create
### `.env` Creation
Create a `.env` file
```bash
touch .env
```
Edit the `.env` file with any editor of your choice
```bash
vim .env
```

### `.env` Template
```
APP_PORT=8082 // Standard port for this microservice
LOG_LEVEL=DEBUG
```
> Additional fields will also be required in the `.env` file to run the microservice successfully. Here is a basic template of the `.env`. Customize to your liking. This template will change as the microservice matures and implements new features.

## Build
You only need to build if you are using docker
<details close>
<summary><h3>With Docker</h3></summary>
<br>

```bash
docker build -t ccu-web-api .
```
</details>


## Install
You only need to install if you are not using docker

<details close>
<summary><h3>Without Docker</h3></summary>
<br>

You will need to install the respective libraries to run this service
```bash
pip install -r requirements.txt
```
</details>

## Run

<details close>
<summary><h3>With Docker</h3></summary>
<br>

Make sure you have a `log.txt` file in the repo directory, otherwise it wont be able to attach the log.txt and will give a warning and sometimes even an error
```bash
touch log.txt
```
Then run the docker image
```bash
./scripts/start.sh
```
or manually with
```bash
docker run -d -e GRADIO_SERVER_NAME=0.0.0.0 -e PYTHONUNBUFFERED=1 $(
if [ -f "$SCRIPT_DIR/../.env" ]; then
    cat "$SCRIPT_DIR/../.env" | grep "APP_PORT" | cut -d= -f2 | awk '{ print "-p "$1":"$1 }'
else
    echo "-p 8082:8082"
fi
) -v $SCRIPT_DIR/../log.txt:/usr/src/app/log.txt --name web-api ccu-web-api
```
</details>

<details close>
<summary><h3>Without Docker</h3></summary>
<br>

```bash
python main.py
```
</details>

### View Docker terminal or unmounted files
If you launched the container using docker, you can execute a sh terminal inside the container to gain access to it and browse around.
```bash
docker exec -it web-api /bin/sh
```
>Leave the shell with `Ctrl+D`

If you want to see the actual go service (the console the `go run ccu` command produces) then
```bash
docker attach web-api
```
> Be careful as it hard to detach as the key bind `Ctrl+P then Ctrl+D` is often used by many programs, so you may not be able to detach correctly.

### Shutting down docker container
If you want to fully shutdown the container
```bash
./scripts/stop.sh
```
or manually with
```bash
docker kill web-api
docker rm web-api
```

