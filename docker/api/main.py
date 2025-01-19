print("API server starting...")
# import packages


# for file operations
import os
# for http server
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
print("imported http functions")

# for db
import psycopg
print("imported psycopg")

# mine for visual clarity
try:
    from posgtres_fucntions import *
    dbapi_test()
except:
    print("failed to import postgres functions")

# not final db column strucutre
'''
table whale (testing)
    id serial primary
    name text
    data integer
table Hunts
    id serial primary
    HuntID text
    TimesCompleted integer
table Users
    id serial primary
    HuntsMade integer
    AsociatedHunts text
'''

# http customizable info
hostName = "0.0.0.0"
serverPort = 5000

'''
# client get function
def GetHuntInfo(HuntNumber):
    with psycopg.connect("dbname=mydb user=master host=slon port=5432") as conn:
        with conn.cursor() as cur:
            cur.execute("") # get the info
            cur.fetchone()
            # now you have the record thin in cur and can send it

# client create hunt action
def CreateHunt(HuntNumber)
    with psycopg.connect("dbname=mydb user=master host=slon port=5432") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM whale WHERE HuntID LIKE HuntNumber") # try if record exists
            try:
            for record in cur:
                print(record)
        except: print("nothing in table")
'''






# --- HTTP Server ---
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/conntest':
            if os.path.exists("conntest.html"):
                self.send_response(200)
                self.send_header("Content-type", "html")  # Adjust MIME type if necessary
                self.end_headers()
                with open("conntest.html", "rb") as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, "File not found")
        if self.path == '/spse':
            return "http://spseplzen.cz"

    def do_HEAD(self):
        if self.path == '/conntest':
            if os.path.exists("conntest.html"):
                self.send_response(200)
                self.send_header("Content-type", "html")  # Adjust MIME type if necessary
                self.end_headers()
            else:
                self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == '/add':  # Endpoint for adding data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                # Call your custom DB function with the parsed data
                response = your_custom_db_function(data)
                self.send_response(200 if response.get('status') == 'success' else 500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())
            except Exception as errorMessage:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(errorMessage)}).encode())

webServer = HTTPServer((hostName, serverPort), MyServer)
print("Server started http://%s:%s" % (hostName, serverPort))
webServer.serve_forever()


'''
for POST

Example Request (cURL):

curl -X POST http://localhost:8080/add \
-H "Content-Type: application/json" \
-d '{"name": "item1", "value": 100}'

✅ Expected Response:

Your custom function should return something like:

{
  "status": "success",
  "message": "Data added successfully"
}
'''





















'''
    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """)

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (100, "abc'def"))

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM test")
        cur.fetchone()
        # will return (1, 100, "abc'def")

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            print(record)

        # Make the changes to the database persistent
        conn.commit()
'''