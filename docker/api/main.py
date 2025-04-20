print("API server starting...")
# import packages


# for http server
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from urllib.parse import urlparse, parse_qs
print("imported http functions")

# for db
import psycopg
print("imported psycopg")


try:
    from psycopg_functions import *
    print("imported psycopg functions")
except:
    print("could not import psycopg functions")

try:
    from http_functions import *
    print("imported http herper functions")
except:
    print("could not import http helper functions")
####################################################################################################################################################################################
####################################################################################################################################################################################

# constants

# http
hostName = "0.0.0.0"
serverPort = 5000

# psycopg
class DBConn:
    name = "mydb"
    user = "master"
    host = "slon"
    port = 5432
connection_data = DBConn()

####################################################################################################################################################################################
####################################################################################################################################################################################



class tableWhaleClass:
    name = "whale"
    columnsList = {
        'id': 'BIGSERIAL PRIMARY KEY',
        'number': 'INTEGER',
        'name': 'TEXT'
    }
    testingData0 = { 'number': 1, 'name': 'uwu' }
    testingData1 = { 'number': 1, 'name': 'owo' }

class tableHuntsClass:
    name = "Hunts"
    columnsList = {
        'id': 'BIGSERIAL PRIMARY KEY',
        'huntid': 'TEXT',
        'count': 'INTEGER'
    }
    testingData0 = { 'huntid': 'MQ==' }
    testingData1 = { 'huntid': 'Mg==' }

class tableUsersClass:
    name = "Users"
    columnsList = { 
        'id': 'BIGSERIAL PRIMARY KEY',
        'userid': 'TEXT'
    }
    testingData0 = { 'userid': 'mqtt' }
    testingData1 = { 'userid': 'spi' }

tableWhale = tableWhaleClass()
tableHunts = tableHuntsClass()
tableUsers = tableUsersClass()

create_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.columnsList)
create_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, tableHunts.columnsList)
create_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableUsers.name, tableUsers.columnsList)

def testFunctions():
    insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.testingData0)
    insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.testingData1)
    insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.testingData1)

    print(fetch_all_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name))
    print(fetch_columns_with_filter(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, ["name", "number"], "name", "owo"))
    print(fetch_columns_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, ["name"]))

testFunctions()

####################################################################################################################################################################################

# formating jsons
def ExtractKeyValue(data, key):
    # Extracts a specific key-value pair from a JSON data
    value = data.get(key)
    return [ { key: value } ]

FindMeServer = HTTPServer((hostName, serverPort), FindMeServerClass)
print("HTTP server started http://%s:%s" % (hostName, serverPort))
FindMeServer.serve_forever()


'''
for POST
Example Request (cURL):

curl -X POST http://localhost:5000/add_hunt -H "Content-Type: application/json" -d '{"column":"data","column":"data"}'

✅ Expected Response:
Your custom function should return something like:
{
  "status": "success",
  "message": "Data added successfully"
}
'''