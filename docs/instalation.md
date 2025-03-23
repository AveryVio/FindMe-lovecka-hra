# Server

Since the server is using docker to run on, any computer powerful enough can run it. It is made to be easy to setup.

First clone this repo and open a terminal window in it's directory. Then run this command:
```sh 
docker-compose build
```
This builds the containers without running them.

If you see and error saying `no configuration file provided: not found` you are in the wrong directory.  
If you are running MS Windows you also may get this error:
```error
unable to get image 'find-me-api': error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.48/images/find-me-api/json": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```
Which means you don't have Docker desktop running.

After that you can run:
```sh
docker-compose up
```
This starts the containers, and builds them if necessary.

Here the same errors apply.

The default configuration works out of the box, however if you wish to, you can configure it according to the [following document](config.md)

# Firmware