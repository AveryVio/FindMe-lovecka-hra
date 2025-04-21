# Server

## Requirements

For using the server all you need an installation of Docker. For Linux only the docker daemon is necessary. For MacOS and MS Windows you need to install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

## Instalation

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

## Requirements

The firmware is compiled in [MPLABX IDE](https://www.microchip.com/en-us/tools-resources/develop/mplab-x-ide) with the [XC32 compiler](https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers/xc32). This software is available for all mainstream operating systems (MS Windows, MacOS and Linux) but there are two external programs that are necessary.  
First You need `sed` a command line tool to edit files, which is used for the changing of the Checkpoint ID. If you use Linux, your distribution may have it preinstalled. If you use MacOS it is preinstalled. On Windows you have to install it yourself (for example using winget)  
Secondly you need Python 3.13+ for interpreting the Checkpoint ID customizing script.