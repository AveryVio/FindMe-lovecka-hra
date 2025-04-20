import psycopg
####################################################################################################################################################################################
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

####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
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
    Fetch specific columns from a table in a PostgreSQL database and return them as dictionaries.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.
        columns (list): List of column names to fetch.

    Returns:
        list: A list of dictionaries where each dictionary represents a row with column-value pairs.
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
                
                # Pair columns with row values
                results = [dict(zip(columns, row)) for row in rows]

                return results

    except (Exception, psycopg.Error) as error:
        print("Error fetching data:", error)
        return None

# fetch rows with filter
def fetch_columns_with_filter(dbname, user, host, port, table_name, columns, filter_column, filter_value):
    """
    Fetch specific columns from a PostgreSQL table and filter by a specified value.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.
        columns (list): List of column names to fetch.
        filter_column (str): Column name to filter by.
        filter_value (str): Value to filter for.

    Returns:
        list: List of dictionaries containing the fetched data.
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
                # Build the SELECT query dynamically
                column_list = ", ".join([f'"{col}"' for col in columns])
                query = f"SELECT {column_list} FROM {table_name} WHERE \"{filter_column}\" = %s;"
                
                cursor.execute(query, (filter_value,))
                results = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in results]
                return result
    
    except (Exception, psycopg.Error) as error:
        print("Error fetching data:", error)
        return []

# fetch specific columns and sort bigges to smallest with an upper limit
def fetch_and_sort(dbname, user, host, port, table_name, columns, sort_column, limit=None):
    """
    Fetches specific columns from a PostgreSQL table,
    sorts the results by a specified column in descending order, and limits the
    number of returned rows.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.
        columns (list): List of column names to fetch.
        sort_column (str): Column to sort the results by (biggest to smallest).
        limit (int, optional): Maximum number of rows to return. Defaults to None (no limit).

    Returns:
        list: List of dictionaries containing the fetched data, sorted by the
              specified column and limited to the specified number of rows.
              Returns an empty list on error.
    """
    try:
        with psycopg.connect(
            dbname=dbname, user=user, host=host, port=port
        ) as conn:
            with conn.cursor() as cursor:
                column_list = ", ".join([f'"{col}"' for col in columns])
                query = (
                    f"SELECT {column_list} FROM {table_name} "
                    f"ORDER BY \"{sort_column}\" DESC"
                )
                if limit is not None:
                    query += f" LIMIT {limit}"
                query += ";"

                cursor.execute(query)
                results = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in results]
                return result

    except (Exception, psycopg.Error) as error:
        print("Error fetching data:", error)
        return []

# check if a hunt exitst
def entry_exists(dbname, user, host, port, table_name, column, value):
    """
    Check if an entry exists in a PostgreSQL table.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.
        column (str): Column name to check.
        value (any): Value to search for in the column.

    Returns:
        bool: True if the entry exists, False otherwise.
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
                # Use parameterized query to prevent SQL injection
                query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {column} = %s);"
                cursor.execute(query, (value,))
                
                return cursor.fetchone()[0]

    except (Exception, psycopg.Error) as error:
        print("Error checking entry:", error)
        return False

# check the amount of total rows
def count_rows(dbname, user, host, port, table_name):
    """
    Counts the number of rows in a PostgreSQL table.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.

    Returns:
        int: The number of rows in the table.  Returns -1 on error.
    """
    try:
        with psycopg.connect(
            dbname=dbname, user=user, host=host, port=port
        ) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT COUNT(*) FROM {table_name};"
                cursor.execute(query)
                count = cursor.fetchone()[0]
                return count

    except (Exception, psycopg.Error) as error:
        print("Error counting rows:", error)
        return -1
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
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

# update funcions
def update_table(dbname, user, host, port, table_name, data, condition):
    """
    Update a specific row in a PostgreSQL table.

    Parameters:
        dbname (str): Database name.
        user (str): Username.
        host (str): Host address.
        port (int): Port number.
        table_name (str): Name of the table.
        data (dict): A dictionary where keys are column names and values are the values to update.
            Example:
                data = {
                    'name': 'Jane Doe',
                    'email': 'jane.doe@example.com'
                }
        condition (dict): A dictionary specifying the WHERE condition.
            Example:
                condition = {'id': 1}

    Returns:
    bool: True if the update was successful, False otherwise.
    """
    try:
        with psycopg.connect(
            dbname=dbname,
            user=user,
            host=host,
            port=port
        ) as conn:
            with conn.cursor() as cursor:
                set_clauses = []
                params = {}

                for col, value in data.items():
                    if isinstance(value, str) and value.startswith(col):  
                        # If value is an expression like "views + 1"
                        set_clauses.append(f'"{col}" = {value}')
                    else:
                        # Normal value update
                        set_clauses.append(f'"{col}" = %({col})s')
                        params[col] = value

                where_clause = " AND ".join([f'"{col}" = %({col})s' for col in condition.keys()])
                params.update(condition)

                query = f'UPDATE {table_name} SET {", ".join(set_clauses)} WHERE {where_clause}'

                cursor.execute(query, params)
                conn.commit()

                print("Row updated successfully!")
                return True

    except (Exception, psycopg.Error) as error:
        print("Error updating data:", error)
        return False