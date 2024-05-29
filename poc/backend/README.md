# Start the docker container (Linux)

## Install the required packages

pip install flask-bcrypt

pip install flask-restplus

pip install Flask-Migrate

pip install pyjwt

pip install Flask-Script

pip install flask_testing

## Build the container

`docker build -t cupola-xs-app .`

## Run the container first time

`docker run -p 5000:5000 --name cupola-xs-container cupola-xs-app`

## Start the container 

`docker start cupola-xs-container`

## Stop the container

`docker stop cupola-xs-container`

## Check the running containers

`docker ps`

## Follow the link

http://127.0.0.1:5000

# Azure (Deployment)

## Install Azure CLI

https://docs.microsoft.com/en-us

## Login to the Azure CLI

`az login`

## Change the subscription if needed

`az account set --subscription <subscription_id>`

`az account list --output table`

## Push the Docker image to the Azure Container Registry

### Login to the registry

`az acr login --name <registry_name>`

ex: `az acr login --name cupola`

### Tag the Docker Image

`docker tag <local_image_name> <registry_name>.azurecr.io/<image_name>:<tag>`

ex: `docker tag cupola-xs-app cupola.azurecr.io/cupola-xs-app:1`

### Push the Docker Image to ACR

`docker push <registry_name>.azurecr.io/<image_name>:<tag>`

ex: `docker push cupola.azurecr.io/cupola-xs-app:1`

## Create a an Azure Container Istance (Deploy the project)
 `az container create     --resource-group <resource_group>    --name <name>     --image <registry_name>.azurecr.io/<image_name>:<tag>     --cpu 1     --memory 1.5     --ip-address public     --ports 5000`

 ex:  `az container create     --resource-group cupola    --name cupola-xs-app     --image cupola.azurecr.io/cupola-xs-app:1     --cpu 1     --memory 1.5     --ip-address public     --ports 5000`

 ## Check the ip address

 `az container show --resource-group cupola --name cupola --query ipAddress.ip`

 ex: `az container show --resource-group cupola --name cupola-xs-app --query ipAddress.ip`

 url_exaple: http://20.61.35.118:5000/



FLASK RESTX BOILER-PLATE WITH JWT BUILD ON PYTHON 3.9
Terminal commands
Note: make sure you have pip and virtualenv installed. To run test: flask test

To run application: flask run
Make sure to run the initial migration commands to update the database (from the venv!).

> export FLASK_APP=manage.py

> flask db init

> flask db migrate

> flask db upgrade
Viewing the app
Open the following url on your browser to view swagger documentation
http://127.0.0.1:5000/
Using Postman / Insomnia
Authorization header is in the following format:

Key: Authorization
Value: "token_generated_during_login"

For testing authorization, url for getting all user requires an admin token while url for getting a single
user by public_id requires just a regular authentication.
Based on : Full description and guide (beware this guide targets an older python version!)
https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563