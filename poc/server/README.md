# Start the docker container (Linux)

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