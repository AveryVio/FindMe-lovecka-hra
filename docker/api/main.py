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

####################################################################################################################################################################################
####################################################################################################################################################################################

# create functions
# create table
def create_table(dbname, user, host, port, table_name, columns):
    """
    Create a custom table in a PostgreSQL database.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the new table.
        columns (dict): A dictionary where keys are column names and values are their SQL types.

    Returns:
    bool: True if the table was created successfully, False otherwise.
    """
    try:
        # Connect to the PostgreSQL database
        with psycopg.connect(
            dbname=dbname,
            user=user,
            host=host,
            port=port
        ) as conn:
            with conn.cursor() as cursor:
                # Build the CREATE TABLE query dynamically
                column_definitions = ", ".join([f'"{col}" {col_type}' for col, col_type in columns.items()])
                query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});"
                
                cursor.execute(query)
                conn.commit()
                
                print(f"Table '{table_name}' created successfully!")
                return True

    except (Exception, psycopg.Error) as error:
        print("Error creating table:", error)
        return False


# fetch functions
# fetch whole table
def fetch_all_from_table(dbname, user, host, port, table_name):
    """
    Fetch all rows from a PostgreSQL table.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.

    Returns:
        list: A list of dictionaries representing the table rows, where keys are column names.
    """
    try:
        # Connect to the PostgreSQL database
        with psycopg.connect(
            dbname=dbname,
            user=user,
            host=host,
            port=port
        ) as conn:
            with conn.cursor() as cursor:
                # Fetch all data from the table
                query = f'SELECT * FROM {table_name}'
                cursor.execute(query)
                
                # Retrieve column names
                col_names = [desc[0] for desc in cursor.description]

                # Fetch all rows and convert them to dictionaries
                rows = cursor.fetchall()
                result = [dict(zip(col_names, row)) for row in rows]
                
                return result

    except (Exception, psycopg.Error) as error:
        print("Error fetching data:", error)
        return False

# fetch specific columns
def fetch_columns_from_table(dbname, user, host, port, table_name, columns):
    """
    Fetch specific columns from a table in a PostgreSQL database.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.
        columns (list): List of column names to fetch.

    Returns:
    list: Rows fetched from the specified columns.
    """
    try:
        # Connect to the PostgreSQL database
        with psycopg.connect(
            dbname=dbname,
            user=user,
            host=host,
            port=port
        ) as conn:
            with conn.cursor() as cursor:
                # Build the query dynamically
                column_list = ", ".join([f'"{col}"' for col in columns])  # Safe column names
                query = f"SELECT {column_list} FROM {table_name};"
                
                cursor.execute(query)
                rows = cursor.fetchall()
                
                return rows

    except (Exception, psycopg.Error) as error:
        print("Error fetching data:", error)
        return None

# fetch rows with filter
def fetch_from_table_with_filter(dbname, user, host, port, table_name, column_name, value):
    """
    Fetch data from a PostgreSQL table based on a filter.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.
        column_name (str): The column to filter by.
        value (str, int, float, etc.): The value to filter by.

    Returns:
        list: A list of dictionaries where each dictionary represents a row in the result set.
        Each dictionary's keys are column names and values are the corresponding values in the row.
    """
    try:
        # Connect to the PostgreSQL database
        with psycopg.connect(
            dbname=dbname,
            user=user,
            host=host,
            port=port
        ) as conn:
            with conn.cursor() as cursor:
                # Build the SELECT query dynamically with filtering
                query = f"""
                    SELECT * 
                    FROM {table_name} 
                    WHERE "{column_name}" = %s
                """
                
                # Execute the query with the given value for filtering
                cursor.execute(query, (value,))
                
                # Fetch all matching rows
                rows = cursor.fetchall()

                # Return the result as a list of dictionaries (one dictionary per row)
                columns = [desc[0] for desc in cursor.description]  # Extract column names
                result = [dict(zip(columns, row)) for row in rows]

                return result

    except (Exception, psycopg.Error) as error:
        print("Error fetching data:", error)
        return []


# insert functions
# insert function
def insert_into_table(dbname, user, host, port, table_name, data):
    """
    Insert data into a PostgreSQL table.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.
        data (dict): A dictionary where keys are column names and values are the values to insert.
            data = {
                'id': 1,
                'name': 'John Doe',
                'email': 'john.doe@example.com'
            }

    Returns:
    bool: True if the insertion was successful, False otherwise.
    """
    try:
        # Connect to the PostgreSQL database
        with psycopg.connect(
            dbname=dbname,
            user=user,
            host=host,
            port=port
        ) as conn:
            with conn.cursor() as cursor:
                # Build the INSERT query dynamically
                columns = ", ".join([f'"{col}"' for col in data.keys()])
                placeholders = ", ".join([f"%({col})s" for col in data.keys()])
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                # Execute the query with data
                cursor.execute(query, data)
                conn.commit()
                
                print("Data inserted successfully!")
                return True

    except (Exception, psycopg.Error) as error:
        print("Error inserting data:", error)
        return False



####################################################################################################################################################################################
####################################################################################################################################################################################



class DBConn:
    name = "mydb"
    user = "master"
    host = "slon"
    port = 5432

class tableWhaleClass:
    name = "whale"
    columnsList = {
        'id': 'BIGSERIAL PRIMARY KEY',
        'number': 'INTEGER',
        'name': 'TEXT'
    }
    testingData0 = {
        'number': 1,
        'name': 'uwu'
    }
    testingData1 = {
        'number': 1,
        'name': 'owo'
    }

class tableHuntsClass:
    name = "Hunts"
    columnsList = {
        'id': 'BIGSERIAL PRIMARY KEY',
        'huntid': 'TEXT'
    }
    testingData0 = {
        'huntid': 'MQ=='
    }
    testingData1 = {
        'huntid': 'Mg=='
    }

class tableUsersClass:
    name = "Users"
    columnsList = {
        'id': 'BIGSERIAL PRIMARY KEY',
        'userid': 'TEXT'
    }
    testingData0 = {
        'userid': 'mqtt'
    }
    testingData1 = {
        'userid': 'spi'
    }

connection_data = DBConn()
tableWhale = tableWhaleClass()
tableHunts = tableHuntsClass()
tableUsers = tableUsersClass()


create_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.columnsList)

insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.testingData0)
insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.testingData1)
insert_into_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, tableWhale.testingData1)


print(fetch_all_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name))
print(fetch_from_table_with_filter(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, "name", "owo"))
print(fetch_columns_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, ["name"]))

####################################################################################################################################################################################



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
            self.send_response(301)
            self.send_header('Location','http://spseplzen.cz')
            self.end_headers()
        
        if self.path == '/i_venture_forth_to_hunt'
            # here goes the return for retrieve hunts
            print("test")

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
print("HTTP server started http://%s:%s" % (hostName, serverPort))
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