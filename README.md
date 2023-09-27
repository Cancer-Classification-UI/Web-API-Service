# Web API Service
This service is responsible for the web interface. Interfaces with all backend API's to facilitate interface logic.

This service will most likely not have an API and wont be used. The web interface can be found at

```
http://<ip>:<APP_PORT>
``` 

If you are running locally it would be at [http://127.0.0.1:7860](http://127.0.0.1:7860)

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
APP_PORT=7860 // Standard port for this microservice
```
> Additional fields will also be required in the `.env` file to run the microservice successfully. Here is a basic template of the `.env`. Customize to your liking. This template will change as the microservice matures and implements new features.

## Install
You will need to install the respective libraries to run this service
```bash
pip install -r requirements.txt
```
## Run
```bash
python main.py
```
