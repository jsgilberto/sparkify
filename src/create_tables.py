""" src/create_tables.py
    This module resets the sparkifydb database.
    To do so:
        - Connects to the default database (required)
        - Drops the sparkifydb database.
        - Creates the sparkifydb database.
        - Drops all tables
        - Creates all tables using sql_queries.py
"""
import psycopg2
import constants
from typing import Text, Tuple, Any
from sql_queries import create_table_queries, drop_table_queries


def reset_database(database_name: Text, user: Text, password: Text) -> None:
    """Resets a database in 3 steps:
        1.- Connects to a *DEFAULT* database and uses the connection to:

        2.- Drop the specified database

        3.- Create a new database with the specified name.

    Args:
        database_name (Text): name of the database to be reset.
        user (Text): user used to connect to the databases.
        password (Text): password used for the user.
    """
    cursor, connection = connect_to_default_database(user, password)
    drop_database(cursor, database_name)
    create_database(cursor, database_name)
    connection.close()


def connect_to_default_database(user: Text, password: Text) -> Tuple[Any, Any]:
    """Attempts to connect to the default postgres database.
    If successful, sets autocommit to True, and creates a cursor.

    Args:
        user (Text): postgres user to use
        password (Text): password of the user

    Returns:
        Tuple[Any, Any]: a cursor and connection objects of the database.
    """
    return connect_to_database("postgres", user, password)


def connect_to_database(
    database_name: Text, user: Text, password: Text
) -> Tuple[Any, Any]:
    """Attempts to connect to a postgres database.
    If successful, sets autocommit to True, and creates a cursor.

    Args:
        database_name (Text): name of the database to connect
        user (Text): postgres user to use
        password (Text): password of the user

    Returns:
        Tuple[Any, Any]: a cursor and connection objects of the database.
    """
    connection = psycopg2.connect(
        f"host=127.0.0.1 dbname={database_name} user={user} password={password}"
    )
    connection.set_session(autocommit=True)
    cursor = connection.cursor()
    return cursor, connection


def create_database(cursor: Any, database_name: Text) -> None:
    """Uses a cursor to create a database

    Args:
        cursor (Any): cursor object returned by psycopg2
        database_name (Text): name of the database to be created
    """
    cursor.execute(
        f"CREATE DATABASE {database_name} WITH ENCODING 'utf8' TEMPLATE template0"
    )


def drop_database(cursor: Any, database_name: Text) -> None:
    """Uses a cursor to drop a database

    Args:
        cursor (Any): cursor object returned by psycopg2
        database_name (Text): name of the database to be dropped
    """
    cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")


def drop_tables(cursor: Any, connection: Any) -> None:
    """Drops each table using the queries in `drop_table_queries` list.

    Args:
        cursor (Any): a cursor object returned by psycopg2
        connection (Any): a connection object returned by psycopg2.connect method
    """
    for query in drop_table_queries:
        cursor.execute(query)
        connection.commit()


def create_tables(cursor: Any, connection: Any) -> None:
    """Creates each table using the queries in `create_table_queries` list.

    Args:
        cursor (Any): a cursor object returned by psycopg2
        connection (Any): a connection object returned by psycopg2.connect method
    """
    for query in create_table_queries:
        cursor.execute(query)
        connection.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database.

    - Establishes connection with the sparkify database and gets
    cursor to it.

    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """
    database_name = "sparkifydb"

    reset_database(
        database_name=database_name,
        user=constants.POSTGRES_USER,
        password=constants.POSTGRES_PASSWORD,
    )

    cursor, connection = connect_to_database(
        database_name=database_name,
        user=constants.POSTGRES_USER,
        password=constants.POSTGRES_PASSWORD,
    )

    drop_tables(cursor, connection)
    create_tables(cursor, connection)

    connection.close()


if __name__ == "__main__":
    main()
