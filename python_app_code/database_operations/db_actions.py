from database_operations import db_config as dbc
from datetime import datetime
import psycopg2

# This script contains basic database function mostly used for basic debugging purposes

def connect(config = None) -> psycopg2.extensions.connection:
    """
    Connects to the PostgreSQL database server.

    Args:
        config (dict): Optional configuration parameters for the connection.

    Returns:
        psycopg2.extensions.connection: The connection object if successful, None otherwise.

    Raises:
        Exception: If there is an error while connecting to the database.
    """
    if config is None:
        config = dbc.load_config()

    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        raise error

def get_today_date(format = '%Y-%m-%d') -> str:
    """
    Returns the current date in the specified format.

    Parameters:
    format (str): Optional. The format in which the date should be returned. Defaults to '%Y-%m-%d'.

    Returns:
    str: The current date in the specified format.

    Example:
    >>> get_today_date()
    '2024-03-03'
    """
    return datetime.today().strftime(format)
    
# The next two functions are for debugging the connection with the db container, they print directly their results to the console
def print_all_tasks():
    """ Retrieve all data from the Tasks table and prints them """

    selec_query = 'SELECT * FROM app."Task"'
    config  = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(selec_query)
                print("Number of %s: %d" % ('Tasks', cur.rowcount))
                row = cur.fetchone()

                while row is not None:
                    print(row)
                    row = cur.fetchone()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def print_all_tasks_with_due_dates():
    """ Retrieve all data from the Tasks table and prints them """

    selec_query = '''SELECT t.id, t.task_name, t.task_descrip, t.creation_date, t.task_status, d.due_date, d.is_active
                        FROM app."Task" AS t JOIN app."Due_by" AS d
                        ON t.id = d.task_id;'''
    config  = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(selec_query)
                print("Number of %s: %d" % ('Tasks', cur.rowcount))
                row = cur.fetchone()

                while row is not None:
                    print(row)
                    row = cur.fetchone()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)