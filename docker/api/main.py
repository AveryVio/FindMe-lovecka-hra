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
    print("imported http helper functions")
except:
    print("could not import http helper functions")

try:
    from api_db_constants import *
    print("imported constants")
except:
    print("could not import constants")

testFunctions()
####################################################################################################################################################################################
####################################################################################################################################################################################

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