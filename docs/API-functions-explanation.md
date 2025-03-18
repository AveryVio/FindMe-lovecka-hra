Here are all functions with their input parameters and a pseudo explanation of their working mechanism.

terms:
cursor: a connection with the database (a psycopg term)
dictionary: a key value pair structure (a python feature)

# DB functions

These functions utilize the psycopg package for operations the postgres database, they all have a specific order generic parameters:

> The connection parameters are in this order and use these types:  
> dbname (str): Database name  
> user (str): Username  
> host (str): Host address  
> port (int): Port number  
> table_name (str): Name of the table  

After this are custom parameters, from now I'll use  "generic_params" as a stand in for this set

## Create functions

create_table
>params: generic_params, columns(dict)  
>returns: True/False  

The function creates a cursor then creates a query by combining the columns and their types. Then it executes the query prints a success message and returns True.
If an error occurs it prints the error message and returns False.

## Fetch functions
#### fetch_all_from_table
> params: generic_params  
> returns: list of dictionaries/False  

The function creates a cursor, then makes a query to get all columns and executes it, then it extracts all column names and combines them with the rows into a list of dictionaries and returns that.
If an error occurs it prints the error message and returns False.
#### fetch_columns_from_table
>params: generic_params, columns(list)  
>returns: list of dictionaries/False  

The function creates a cursor and makes a query from column names, then executes it. Then It combines rows and columns them into dictionaries in a list and returns.
If an error occurs it prints the error message and returns False.
#### fetch_columns_with_filter
>params: generic_params, columns(list), filter_column(str), filter_value(str)  
>returns: list of dictionaries/Empty list  

The function creates a cursor and makes a column list string that it inserts into a query, then executes it. Then it turns the returned values into a list of dictionaries and returns that.
If an error occurs it prints the error message and returns an empty list.
#### entry_exists
>params: generic_params, column(str), value(str)  
>returns: True/False  

The function creates a cursor and makes a query filtering for the value in a specific column, then executes it and returns the output.
If an error occurs it prints the error message and returns False.
## Insert functions
#### insert_into_table
>params: generic_params, data(dict)  
>returns: True/False  

The function creates a cursor and joins the columns and rows into a query that it then executes. If no error occurs, it returns True.
If an error occurs it prints the error message and returns False.

## Update functions
#### update_table
>params: generic_params, data(dict)  
>returns: True/False  

The function creates a cursor and joins the columns and rows into a query that it then executes. If no error occurs, it returns True.
If an error occurs it prints the error message and returns False.

----

# HTTP functions

The HTTP server has several internal functions to define the behaviour of responding to HTTP requests.
This project only uses two and that's GET and POST. Both respond on specific URI paths and those will be discussed separately.
There are also some helper functions to make the responses more unified and the code more readable.

## Helper cunctions

#### ExtractKeyValue
>params: data(dict), key(str)
>returns: dictionary containing the key and value of data

The function takes in the parameters and extracts the value corresponding to key, then it makes the pair into a dictionary.

#### SendJSONResponse
>params: self(obj), data(dict)

The function makes the headers with the HTTP status, then it sends the data as a JSON response.

#### SendJSONQueryResponse
>params: self(obj), response(dict)

The function makes the headers with the HTTP status and Access Control Allow Methods as POST, then it sends the data as a JSON response.

#### SendJSONError
>params: self(obj), errorM(Exception)

The function makes the headers with the HTTP status, then it sends the error as a JSON response.

#### SendHTMLResponse
>params: self(obj), message(str)

The function makes the headers with the HTTP status, then it sends the message as an HTML response.

## do_GET
>params: self(obj)

#### /conntest

For testing if the HTTP server is up without having to rely on psycopg working, basically a fancy ping.
#### /add

For GET requests this page only serves to tell a lost traveller that this is a POST only path.
#### /i_venture_forth_to_hunt

The function separates the parameters from the path. If the parameters are empty or incorrect, it responds with an error message.
If they're correct they separate the key value pairs into a list of dictionaries, then it then uses fetch_columns_with_filter() to get the desired data and sends it to the client as a JSON file.
If an error occurs, it send's that message to the client.

#### /spse

This page is just a redirect to my schools website. That's it.

## do_POST
>params: self(obj)

#### /add_hunt

First, the function checks if the hunt exists in the database using entry_exists(). If it does, then it increments the count column of the hunt using update_table(), if it doesn't exist, then it adds the hunt to the database using insert_into_table(). After the request is resolved then it sends a confirmation to the user.
If an error occurs, then the server sends it to the user.

#### /add_user

>[!WARNING]
>this is not supported right now

The function loads the JSON data and inserts the user into the database, after that if sends a confirmation to the user.
If an error occurs, the server sends the user a message containing it.