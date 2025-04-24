# Design considerations

## Server

I chose to host the server on an instance of Docker, to make it behave consistently on all hosting machines. Since there are two services, I used Docker Compose to be able to manage both easier.  
For a database i chose Postgres because of it's popularity and therefore support and compatibility. I do not use much special types that it's known for, since that would make the handling of data more difficult.  
For making the API for the app i used python and made a script for handling database operations and communication with the clients. The script uses the internal python http server library, and sends and receives data with the JSON library. I chose to use those two, because the documentation for their use was the most extensive out of the options i found. For database operations I chose the psycopg library, because it is the recommended option for utilizing Postgres with python.

## Firmware

For the firmware I chose to use MPLAB X IDE, since it was recommended by my teachers.  
For changing the Bluetooth device ID I needed an external program, because executing shell commands from the Makefile of the project caused inconsistent behaviour. (sometimes the replacing of text would fail) I chose python since it was already used for the server and it's cross platform. Within the actual script I use the standard sed utility, which is installed by default on Linux and Mac. Not on Windows but this utility is easily installed using Winget.  

# Project structure comments

## Server

The server uses Postgres with one table for hunts. The table uses an internal id, however every row has a huntid, that is calculated by the client from the ID's of the checkpoints.  
The API script uses a JSON file the client POSTs for adding hunt's instead of url parameters, because that prevents the client from sending incorrect data, since Javascript has it's own handling of data that way. This is not done in GET, where url parameters are used, since they're faster for processing. They are easier to mess up within the client, but that is not a problem here, since that doesn't risk corrupting DB data.  

## Firmware

/* firmware not finalized*/