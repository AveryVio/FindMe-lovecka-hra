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


import helper.psycopg_functions as dbf
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

dbf.create_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.columnsList)
dbf.create_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, tableHunts.columnsList)
dbf.create_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableUsers.name, tableUsers.columnsList)

def testFunctions():
    dbf.insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.testingData0)
    dbf.insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.testingData1)
    dbf.insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.testingData1)

    print(dbf.fetch_all_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name))
    print(dbf.fetch_columns_with_filter(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, ["name", "number"], "name", "owo"))
    print(dbf.fetch_columns_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, ["name"]))

testFunctions()

####################################################################################################################################################################################

# formating jsons
def ExtractKeyValue(data, key):
    # Extracts a specific key-value pair from a JSON data
    value = data.get(key)
    return [ { key: value } ]

def SendJSONResponse(self, data):
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(data).encode('utf-8'))

def SendJSONQueryResponse(self, response):
    self.send_response(200) # if i need this could handle an error ==> if response.get('status') == True else 500
    self.send_header('Content-Type', 'application/json')
    self.send_header("Access-Control-Allow-Methods", "POST")
    self.end_headers()
    self.wfile.write(json.dumps(response).encode())

def SendJSONError(self, errorM):
    self.send_response(500)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps({"error": str(errorM)}).encode('utf-8'))

def SendHTMLResponse(self, message):
    self.send_response(200)
    self.send_header("Content-type", "html")  # Adjust MIME type if necessary
    self.end_headers()
    self.wfile.write(bytes(message,"utf-8"))

# HTTP Server
class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        query = urlparse(self.path).query
        parsed_path = urlparse(self.path)

        # connection testing path
        if parsed_path.path == '/conntest':
            SendHTMLResponse(self, "<head><title>YYYYYYEEEEEEEESSSSSSSSSSS</title></head><body><p>Hewwo Wowld! :3 </p><p>If you're reading this the server is online</p></body></html>")

        # path for adding
        if parsed_path.path == '/add_hunt':
            SendHTMLResponse(self, "<html><body><p>this is only for data input</p></body></html>")

        # path for fetching data
        if parsed_path.path == '/i_venture_forth_to_hunt':
            # test for missing prams
            if query == "":
                SendJSONError(self, "missing params")
            else:
                # handle the filtered params
                if (query[0] == "f"):
                    try:
                        # parse params to get seperate data params
                        filter_params = []
                        for queryUnit in query.split("&"):
                            querySubunits = queryUnit.split("=")
                            filter_params.append({querySubunits[0]: querySubunits[1]})
                        # use db to get data and put it into a list
                        data = []
                        dataUnit = ""
                        for filter_param in filter_params:
                            dataUnit = dbf.fetch_columns_with_filter(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, ["huntid", "count"], "huntid", filter_param["f"])
                            data.append(dataUnit)
                            dataUnit = ""
                        print("fetch data:" + str(data))
                        SendJSONResponse(self, data)
                    except Exception as errorM:
                        SendJSONError(self, errorM)
                # handle the catchall param
                elif query[0] == "*":
                    try:
                        data = dbf.fetch_all_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name)
                        SendJSONResponse(self, data)
                    except Exception as errorM:
                        SendJSONError(self, errorM)
                # report bad prams
                else:
                    SendJSONError(self, "bad params")

        # spse promo
        if parsed_path.path == '/spse':
            self.send_response(301)
            self.send_header('Location','http://spseplzen.cz')
            self.end_headers()


    def do_POST(self):
        # Endpoint for adding hunts
        if self.path == '/add_hunt':
            # get the json
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                # parse the request json
                data = json.loads(post_data)
                counting_list = ExtractKeyValue(data, "huntid")
                for entry in counting_list:
                    # check if entry exists, if yes then increment the count
                    if dbf.entry_exists(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, "huntid", entry["huntid"]):
                        response_result = dbf.update_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, {"count":"count +1"}, data)
                    # if not then add the hunt
                    else:
                        data_plus_count1 = {**data, **{"count":1}}
                        response_result = dbf.insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, data_plus_count1)
                response = {"get":response_result}
                # send the response
                SendJSONQueryResponse(self, response)
            except json.JSONDecodeError as errorM:
                SendJSONError(self, errorM)
            except Exception as errorM:
                SendJSONError(self, errorM)


        # Endpoint for adding users
        if self.path == '/add_user':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                response_result = dbf.insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableUsers.name, data)
                response = {"get":response_result}
                SendJSONQueryResponse(self, response)
            except json.JSONDecodeError as errorM:
                SendJSONError(self, errorM)
            except Exception as errorM:
                SendJSONError(self, errorM)

webServer = HTTPServer((hostName, serverPort), MyServer)
print("HTTP server started http://%s:%s" % (hostName, serverPort))
webServer.serve_forever()


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