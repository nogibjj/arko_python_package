from databricks import sql
from mypackage.query import create, read, update, delete
from dotenv import load_dotenv
import os


load_dotenv()
databricks_key = os.getenv("DATABRICKS_KEY")
server_host_name = os.getenv("SERVER_HOST_NAME")
sql_http = os.getenv("SQL_HTTP")


def reset_database():
    with sql.connect(
        access_token=databricks_key,
        server_hostname=server_host_name,
        http_path=sql_http,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS AAPL")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS AAPL (
                    DATE DATE,
                    OPEN FLOAT,
                    HIGH FLOAT,
                    LOW FLOAT,
                    Close FLOAT,
                    VOLUME BIGINT
                )
                """
            )


def test_create_entry():
    reset_database()
    entry = ("2024-10-06", 100.0, 110.0, 95.0, 105.0, 100000)
    result = create(entry)
    assert result == "Entry added successfully!"

    with sql.connect(
        access_token=databricks_key,
        server_hostname=server_host_name,
        http_path=sql_http,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM AAPL WHERE DATE = '2024-10-06'")
            data = cursor.fetchone()

    converted_data = (
        str(data.DATE),
        data.OPEN,
        data.HIGH,
        data.LOW,
        data.Close,
        data.VOLUME,
    )

    assert converted_data == entry, f"Expected {entry}, but got {converted_data}"


def test_read_entries():
    reset_database()
    entry = ("2024-10-06", 100.0, 110.0, 95.0, 105.0, 100000)
    create(entry)

    result = read()
    print("result", result)
    assert result == "Success"


def test_update_entry():
    reset_database()
    entry = ("2024-10-06", 100.0, 110.0, 95.0, 105.0, 100000)
    create(entry)

    result = update("OPEN", 120.0, "DATE", "2024-10-06")
    assert result == "Entry updated successfully!"

    with sql.connect(
        access_token=databricks_key,
        server_hostname=server_host_name,
        http_path=sql_http,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT OPEN FROM AAPL WHERE DATE = '2024-10-06'")
            data = cursor.fetchone()

    assert data[0] == 120.0, f"Expected OPEN = 120.0, but got {data[0]}"


def test_delete_entry():
    reset_database()
    entry = ("2024-10-06", 100.0, 110.0, 95.0, 105.0, 100000)
    create(entry)

    result = delete("DATE", "2024-10-06")
    assert result == "Entry deleted successfully!"

    with sql.connect(
        access_token=databricks_key,
        server_hostname=server_host_name,
        http_path=sql_http,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM AAPL WHERE DATE = '2024-10-06'")
            data = cursor.fetchone()

    assert data is None, f"Expected None, but got {data}"


if __name__ == "__main__":
    test_create_entry()
    test_read_entries()
    test_update_entry()
    test_delete_entry()

    print("All tests passed!")
