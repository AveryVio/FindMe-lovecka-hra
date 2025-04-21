from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from urllib.parse import urlparse, parse_qs

from psycopg_functions import *
from api_db_constants import *

####################################################################################################################################################################################
####################################################################################################################################################################################
# formating jsons
def ExtractKeyValue(data, key):
    # Extracts a specific key-value pair from a JSON data
    value = data.get(key)
    return [ { key: value } ]

def SendJSONResponse(self, data):
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    self.wfile.write(json.dumps(data).encode('utf-8'))

def SendJSONQueryResponse(self, response):
    self.send_response(200) # if i need this could handle an error ==> if response.get('status') == True else 500
    self.send_header('Content-Type', 'application/json')
    self.send_header("Access-Control-Allow-Methods", "POST")
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    self.wfile.write(json.dumps(response).encode())

def SendJSONError(self, errorM):
    self.send_response(500)
    self.send_header("Content-Type", "application/json")
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    self.wfile.write(json.dumps({"error": str(errorM)}).encode('utf-8'))

def SendHTMLResponse(self, message):
    self.send_response(200)
    self.send_header("Content-type", "html")  # Adjust MIME type if necessary
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    self.wfile.write(bytes(message,"utf-8"))
####################################################################################################################################################################################
####################################################################################################################################################################################
# HTTP Server
class FindMeServerClass(BaseHTTPRequestHandler):

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
                        # get and send
                        data = []
                        dataUnit = ""
                        for filter_param in filter_params:
                            dataUnit = fetch_columns_with_filter(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, ["huntid", "count"], "huntid", filter_param["f"])
                            data.append(dataUnit)
                            dataUnit = ""
                        print("fetch data:" + str(data))
                        SendJSONResponse(self, data)
                    except Exception as errorM:
                        SendJSONError(self, errorM)
                # handle the top completed hunts
                elif query[0] == "t":
                    try:
                        # parse amount
                        amount = ""
                        for i in query:
                            if (i == "t") or (i == "="):
                                continue
                            amount = amount + i
                        # cap amount by the amount of rows in the db
                        max_amount = count_rows(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name)
                        if int(max_amount) > int(amount):
                            amount = max_amount
                        # get and send data
                        data = fetch_and_sort(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, ["huntid", "count"], "count", amount)
                        SendJSONResponse(self, data)
                    except Exception as errorM:
                        print(errorM)
                        SendJSONError(self, errorM)
                # handle the catchall param
                elif query[0] == "*":
                    try:
                        data = fetch_all_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name)
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

####################################################################################################################################################################################
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
                    if entry_exists(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, "huntid", entry["huntid"]):
                        response_result = update_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, {"count":"count +1"}, data)
                    # if not then add the hunt
                    else:
                        data_plus_count1 = {**data, **{"count":1}}
                        response_result = insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableHunts.name, data_plus_count1)
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
                response_result = zinsert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableUsers.name, data)
                response = {"get":response_result}
                SendJSONQueryResponse(self, response)
            except json.JSONDecodeError as errorM:
                SendJSONError(self, errorM)
            except Exception as errorM:
                SendJSONError(self, errorM)