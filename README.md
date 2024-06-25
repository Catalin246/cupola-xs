# Cupola-xs

This repository contains the code for the AI project requested by Cupola XS in Haarlem. 
The project entails the use of AI and Machine Learning to predict visitor numbers based on the following historical data:
1. Total Connected Devices to the Cupola Wi-Fi
2. Total Cinema Visitors

Using this data, an LSTM time-series model is build to give predictions. The front-end interface also allows you to upload new data for re-training, and model rollback.

## Project Structure
This repository contains both the front-end and back-end, however they are separetely containerized using Docker.
Backend is located at 'poc/backend' and Frontend is located at 'poc/frontend'.

The backend folder contains an additional README file containing backend-specific information.

## Prerequisites
### Ensure that Docker is installed and running on your system.

## Open the Terminal
1. Navigate to the project directory:

`cd poc`

## Build the Container
2. Build the container:

`docker compose up --build`

## Run the Created Container
3. Run the container:

`docker compose up`

## Stop the Container
4. Stop the container:
Press Ctrl + C in the terminal where the container is running.