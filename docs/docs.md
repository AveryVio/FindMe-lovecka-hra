# server

The server runs on containers through Docker Compose, currently there are two containers, one for the database and one containing the python made API.  
The explanation of every function is [here](API-functions-explanation.md).

## DB

This project uses Postgres as the database of choice, which as stated runs on a separate container from the API. It's environment variables are stated in the Docker Compose file, containing the database name and user. For now it uses no auth for ease of access, but for the future auth will get added.

Layout of the database is not final, however the current iteration has this composition:

TableWhale - testing table (for startup tests)

| column | id                    | number  | name |
| ------ | --------------------- | ------- | ---- |
| type   | BIGSERIAL PRIMARY KEY | INTEGER | TEXT |
TableHunts - primary table for storing hunt hashes

| column | id                    | huntid | count   |
| ------ | --------------------- | ------ | ------- |
| type   | BIGSERIAL PRIMARY KEY | TEXT   | INTEGER |
>huntid stores the identification hash for each hunt, while the id is a unique identifier in the database (this is a precaution to stop any error scenarios in the future)
>count stores the amount of times the hunt has been completed, starting at 1

TableUsers - to be developed on (will be for storing users for analytics and mabye a login system)

| column | id                    | userid |
| ------ | --------------------- | ------ |
| type   | BIGSERIAL PRIMARY KEY | TEXT   |
>userid stores the identification hash for each user, while the id is a unique identifier in the database (this is a precaution to stop any error scenarios in the future)


## API

The API is built using Python, utilizing standard packages and [psycopg3](https://psycopg.org/) for communicating with the database, and hosting the http/https server. 

The server communicates directly with the client through http/https, the format of communication is discussed [here](communication.md). Communication between the API and DB is through internal network, however that is beyond the scope of this documentation, you can learn more in the [psycopg3 documentation](https://www.psycopg.org/psycopg3/docs/).

----
# firmware
