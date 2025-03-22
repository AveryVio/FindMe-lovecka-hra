# Server

Jelikož server používáme docker, může být spuštěný na jakémkoli počítači, který je  dostatečně výkonný. Je vytvořen aby byl jednoduchý spustit.

Po klonování repositáře otevřete okno příkazové řádky v jeho adresáři. Poté použijte tento příkaz:
```sh 
docker-compose build
```
To postaví kontejnery bez spuštění.

Když vidíte chybu `no configuration file provided: not found` jste ve špatném adresáři.  
Když server spouštíte na počítači s MS Windows také může nastat chybu:
```error
unable to get image 'find-me-api': error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/v1.48/images/find-me-api/json": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```
To znamená že nemáte spuštěný Docker desktop.

Poté můžete spustit:
```sh
docker-compose up
```
Což spustí kontejnery a postaví je jestli je potřeba.

U tohoto platí stejné chyby.

Základní nastavení funguje od začátku, ale pokud chcete, můžete ho nastavit podle [následujícího dokumentu](konfiguraceCZ.md)

# Firmware