from psycopg_functions import *

####################################################################################################################################################################################
# connections
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
# db tables
class tableWhaleClass:
    name = "whale"
    columnsList = {
        'id': 'BIGSERIAL PRIMARY KEY',
        'number': 'INTEGER',
        'name': 'TEXT'
    }
    testingData0 = { 'number': 1, 'name': 'uwu' }
    testingData1 = { 'number': 10, 'name': 'owo' }

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

####################################################################################################################################################################################
# db tests

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

    update_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, {"number":"number +1"}, {"name":"owo"})

    print(fetch_all_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name))
    print(fetch_columns_with_filter(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, ["name", "number"], "name", "owo"))
    print(fetch_columns_from_table(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, ["name"]))
    print(fetch_and_sort(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, ["name", "number"], "name", 5))
    print(entry_exists(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name, "name", "owo"))
    print(count_rows(connection_data.name, connection_data.user, connection_data.host, connection_data.port, tableWhale.name))

