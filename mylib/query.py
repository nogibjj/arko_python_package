from databricks import sql
from tabulate import tabulate
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()
databricks_key = os.getenv("DATABRICKS_KEY")
server_host_name = os.getenv("SERVER_HOST_NAME")
sql_http = os.getenv("SQL_HTTP")


def create(entry):
    """
    Insert a new entry into the AAPL table.

    Parameters:
    - entry: A tuple containing the values to insert into the table
    """
    with sql.connect(
        access_token=databricks_key,
        server_hostname=server_host_name,
        http_path=sql_http,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO AAPL VALUES (?, ?, ?, ?, ?, ?)", entry)
    return "Entry added successfully!"


def read():
    """
    Read the first 5 rows from the AAPL table.
    """
    with sql.connect(
        access_token=databricks_key,
        server_hostname=server_host_name,
        http_path=sql_http,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM AAPL LIMIT 5")

            # Fetch all rows and get the column names
            results = cursor.fetchall()
            headers = [description[0] for description in cursor.description]

            # Display results as a table
            print("Query Results:")
            print(tabulate(results, headers, tablefmt="pretty"))
    return "Success"


def custom_query(
    query="""WITH PriceData AS (
    SELECT 
        CAST(Date AS DATE) AS Date,  
        CAST(Open AS FLOAT) AS Open,      
        CAST(High AS FLOAT) AS High,      
        CAST(Low AS FLOAT) AS Low,        
        CAST(Close AS FLOAT) AS Close,    
        CAST(Volume AS BIGINT) AS Volume, 
        (CAST(High AS FLOAT) - CAST(Low AS FLOAT)) AS price_range,  
        SUM(CAST(Volume AS BIGINT)) OVER() AS total_volume,  
        AVG(Close) OVER (ORDER BY Date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_close
    FROM 
        aapl
)
SELECT 
    Date, 
    Open, 
    High, 
    Low, 
    Close, 
    Volume, 
    price_range, 
    moving_avg_close, 
    total_volume
FROM 
    PriceData
ORDER BY 
    Date ASC
LIMIT 10;
""",
):
    """
    Run a custom query on the AAPL table.

    Parameters:
    - query: A string query for custom querying the table.
    """
    with sql.connect(
        access_token=databricks_key,
        server_hostname=server_host_name,
        http_path=sql_http,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)

            # Fetch all rows and get the column names
            results = cursor.fetchall()
            headers = [description[0] for description in cursor.description]

            # Display results as a table
            print("Query Results:")
            print(tabulate(results, headers, tablefmt="pretty"))
    return "Success"


def update(column, new_value, condition_column, condition_value):
    """
    Update a specific value in the AAPL table.

    Parameters:
    - column: The column to update.
    - new_value: The new value to set in the column.
    - condition_column: The column to check in the WHERE condition.
    - condition_value: The value in the condition_column to match for updating.
    """
    with sql.connect(
        access_token=databricks_key,
        server_hostname=server_host_name,
        http_path=sql_http,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE AAPL SET {column} = ? WHERE {condition_column} = ?",
                (new_value, condition_value),
            )
    return "Entry updated successfully!"


def delete(condition_column, condition_value):
    """
    Delete a row from the AAPL table.

    Parameters:
    - condition_column: The column to check in the WHERE condition.
    - condition_value: The value in the condition_column to match for deletion.
    """
    with sql.connect(
        access_token=databricks_key,
        server_hostname=server_host_name,
        http_path=sql_http,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM AAPL WHERE {condition_column} = ?", (condition_value,)
            )
    return "Entry deleted successfully!"
