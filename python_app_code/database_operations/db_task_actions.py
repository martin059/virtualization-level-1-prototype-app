from database_operations import db_config as dbc, db_actions as dba
from datetime import datetime
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from typing import Optional, Tuple

def get_all_tasks() -> list:
    """ Retrieve all data from the Tasks table.

    Returns:
        list: A list of dictionaries representing the rows retrieved from the Tasks table.
              Each dictionary contains the column names as keys and the corresponding values as values.
              Returns None if an error occurs during the database operation.

    Raises:
        Exception: If there is an error while executing the SQL query or connecting to the database.
    """

    select_query = 'SELECT * FROM app."Task" ORDER BY id ASC'
    config  = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(select_query)
                return cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error
    
def get_a_task(task_id: str) -> list:
    """
    Retrieve one task from the Tasks table.

    Args:
        task_id (str): The ID of the task to retrieve.

    Returns:
        list: A list of dictionaries representing the retrieved task(s).
              Each dictionary contains the column names as keys and the corresponding values.

    Raises:
        Exception: If there is an error while executing the SQL query or connecting to the database.

    """
    select_query_base = 'SELECT * FROM app."Task" WHERE id = {0}'
    select_query = sql.SQL(select_query_base).format(sql.Literal(task_id))
    config  = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(select_query)
                return cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error
    
def insert_into_task_table(task_name: str, task_descrip: str = None, creation_date: str = None,
                            task_status: str = None, due_date: str = None) -> int:
    """Inserts a new task into the database and returns the new task's ID.

    Args:
        task_name (str): The name of the task.
        task_descrip (str, optional): The description of the task. Defaults to None.
        creation_date (str, optional): The creation date of the task. Defaults to None.
        task_status (str, optional): The status of the task. Defaults to None.
        due_date (str, optional): The due date of the task. Defaults to None.

    Returns:
        int: The ID of the newly inserted task.

    Raises:
        Exception: If there is an error while executing the SQL query or connecting to the database.

    """
    str = dba.compose_task_insert_update_values(task_name, task_descrip, creation_date, task_status)

    # Doc about how to compose SQL https://www.psycopg.org/docs/sql.html
    insert_query_base = "INSERT INTO app.\"Task\"({columns}) VALUES({values}) RETURNING id;"
    insert_query = sql.SQL(insert_query_base).format(
                        columns=sql.SQL(',').join(map(sql.Identifier, str[0])),
                        values=sql.SQL(',').join(map(sql.Literal, str[1]))
                    )

    new_id = None
    config = dbc.load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # print(insert_query.as_string(conn)) # DEBUG
                # execute the INSERT statement
                cur.execute(insert_query)

                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    new_id = rows[0]

                # commit the changes to the database
                conn.commit()

            # if due date is provided, insert it
            if due_date is not None:
                dba.insert_due_date(conn, new_id, due_date)
            
            return new_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error

def update_task(task_id: str, task_name: str = None, task_descrip: str = None,
                 task_creation_date: str = None, task_status: str = None, due_date: str = None) -> None:
    """
    Updates the data of a Task including its possible due-date.

    Args:
        task_id (str): The ID of the task to be updated.
        task_name (str, optional): The new name of the task. Defaults to None.
        task_descrip (str, optional): The new description of the task. Defaults to None.
        task_creation_date (str, optional): The new creation date of the task. Defaults to None.
        task_status (str, optional): The new status of the task. Defaults to None.
        due_date (str, optional): The new due date of the task. Defaults to None.

    Returns:
        None: Returns None if the task is successfully updated.

    Raises:
        Exception: Raises an exception if there is an error during the update process.
    """
    update_query_base = 'UPDATE app."Task" SET {0} WHERE id = {1}'
    str = dba.compose_task_insert_update_values(task_name, task_descrip, task_creation_date, task_status)
    update_query = sql.SQL(update_query_base).format(
                        sql.SQL(',').join(map(lambda x: sql.SQL('{0} = {1}').format(sql.Identifier(x[0]), sql.Literal(x[1])), zip(str[0], str[1]))),
                        sql.Literal(task_id)
                    )
    config = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            # return update_query.as_string(conn) # DEBUG
            with conn.cursor() as cur:
                cur.execute(update_query)
                conn.commit()

                # if due date is provided, insert it
                if due_date is not None:
                    dba.insert_into_due_by_table(task_id, due_date)

                return None
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error

def delete_task(task_id: str) -> None:
    """Updates the state of a Task to be 'DELETED'.

    Args:
        task_id (str): The ID of the task to be deleted.

    Raises:
        Exception: If an error occurs during the deletion process.

    Returns:
        None
    """
    update_query_base = 'UPDATE app."Task" SET task_status = \'Deleted\' WHERE id = {0}'
    update_query = sql.SQL(update_query_base).format(sql.Literal(task_id))
    config = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            print(update_query.as_string(conn))
            with conn.cursor() as cur:
                cur.execute(update_query)
                conn.commit()
                return None

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error