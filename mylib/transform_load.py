from databricks import sql
import csv
import os
from dotenv import load_dotenv

def load(dataset="data/AAPL.csv"):
    # print(f"Current working directory: {os.getcwd()}")

    load_dotenv()
    databricks_key = os.getenv("DATABRICKS_KEY")
    server_host_name = os.getenv("SERVER_HOST_NAME")
    sql_http = os.getenv("SQL_HTTP")

    with open(dataset, newline="") as csvfile:
        payload = list(csv.reader(csvfile, delimiter=","))
        
        header = payload[0]
        formatted_header = ['Close' if col == 'Close(t)' else col for col in header[:6]]

        # print(f"Formatted Header: {formatted_header}")

        last_100_rows = payload[-101:]
        # print(f"Last 100 Rows: {last_100_rows}")

        with sql.connect(
            access_token=databricks_key,
            server_hostname=server_host_name,
            http_path=sql_http,
        ) as connection:
            with connection.cursor() as cursor:
                
                cursor.execute("SHOW TABLES FROM default LIKE 'AAPL*'")
                result = cursor.fetchall()
                if result:
                    cursor.execute("DROP TABLE IF EXISTS AAPL")

                columns = ", ".join([f"{col} STRING" for col in formatted_header])
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS AAPL (
                    {columns}
                )
                """
                cursor.execute(create_table_query)

                insert_query = f"INSERT INTO AAPL ({', '.join(formatted_header)}) VALUES ("

                for i, row in enumerate(last_100_rows[1:]):

                    print(f"Inserting Row: {i+1}")
                    if len(row) < 6:
                        print(f"Skipping row due to insufficient data: {row}")
                        continue

                    formatted_values = ", ".join([f"'{value}'" if isinstance(value, str) else str(value) for value in row[:6]])
                    cursor.execute(insert_query + formatted_values + ")")


        print("Last 100 rows from the CSV file have been successfully loaded into Databricks")
        return "Databricks SQL database updated"

