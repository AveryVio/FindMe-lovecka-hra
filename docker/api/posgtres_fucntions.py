def dbapi_test():
    print("functions for PostgeSQL imported")
    return True

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

# fetch column row filter combo
def fetch_from_table(dbname, user, host, port, table_name, column_name, value):
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

#insert functions
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
