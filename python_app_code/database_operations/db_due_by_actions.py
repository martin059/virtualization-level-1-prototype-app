from database_operations import db_config as dbc
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from typing import Optional, Tuple

# This script defines all operations that can be done on the Due_by table

def get_due_by(task_id: str) -> list:
    """
    Retrieve all due dates of a given task from the Due_by table.

    Args:
        task_id (str): The ID of the task.

    Returns:
        list: A list of dictionaries representing the rows retrieved from the Due_by table.
              Each dictionary contains the column names as keys and the corresponding values.

    Raises:
        Exception: If there is an error while executing the SQL query or connecting to the database.

    """
    select_query_base = 'SELECT * FROM app."Due_by" WHERE task_id = {0}'
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

def get_specific_due_by(task_id: str, due_date: str) -> list:
    """ Retrieve a specific due date of a given task from the Due_by table.

    Args:
        task_id (str): The ID of the task.
        due_date (str): The due date of the task.

    Returns:
        list: A list of dictionaries representing the rows retrieved from the "Due_by" table.
              Each dictionary contains the column names as keys and the corresponding values.

    Raises:
        Exception: If there is an error while executing the SQL query or connecting to the database.
    """

    select_query_base = 'SELECT * FROM app."Due_by" WHERE task_id = {0} AND due_date = {1}'
    select_query = sql.SQL(select_query_base).format(sql.Literal(task_id), sql.Literal(due_date))
    config  = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(select_query)
                return cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error

def insert_due_date(conn: psycopg2.extensions.connection, task_id: int, due_date: str) -> None:
    """
    Inserts a due date for a task into the database.

    Args:
        conn (psycopg2.extensions.connection): The database connection object.
        task_id (int): The ID of the task.
        due_date (str): The due date of the task.

    Returns:
        None: If the due date was successfully inserted.

    Raises:
        Exception: If there is an error while executing the SQL query or connecting to the database.

    """
    insert_query_base = "INSERT INTO app.\"Due_by\"({columns}) VALUES({values});"
    insert_query = sql.SQL(insert_query_base).format(
                        columns=sql.SQL(',').join(map(sql.Identifier, ("task_id", "due_date"))),
                        values=sql.SQL(',').join(map(sql.Literal, (task_id, due_date)))
                    )
    
    # print(insert_query.as_string(conn)) # DEBUG
    try:
        with  conn.cursor() as cur:
            cur.execute(insert_query, (task_id, due_date))
            conn.commit()
            return None
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error

def insert_into_due_by_table(task_id: int, due_date: str) -> str:
    """
    Insert or update a due date for a task in the Due_by table.

    Parameters:
    - task_id (int): The ID of the task.
    - due_date (str): The new due date to be inserted or updated.

    Logic:
    1. Check if the task has an active due date.
    2. If there is an active due date and the new due date is different from the active one,
       update the corresponding row to set 'is_active' to False.
    3. If the new due date is the same as the active one, end the process.
    4. Check if the new due date is already present in the table with 'is_active' set to False.
       If it is, update that row to set 'is_active' to True.
    5. If the new due date is not present, add a new row with the new due date and set 'is_active' to True.

    Raises:
        Exception: If an error occurs during the deletion process.
    
    Returns:
    - str: A message indicating the result of the operation.
    """
    select_query, update_deactivate_query, update_activate_query, insert_query = prep_insert_due_date_queries(task_id, due_date)
    config = dbc.load_config()
    msg: Optional[str] = None
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Check if the task has an active due date
                cur.execute(select_query)
                rows = cur.fetchall()
                modification_necessary: bool = True
                due_date_already_present: bool = False
                if rows:
                    modification_necessary, due_date_already_present, msg = check_current_due_date(cur, rows, due_date,
                                                                                                    update_deactivate_query)
                # If modification is necessary, and due date is already present, activate row
                if modification_necessary:
                    if due_date_already_present:
                        cur.execute(update_activate_query)
                        msg = f"Updated active due date for task id: {task_id}"
                    else:
                        # If modification is necessary, and new due date is not present, insert a new row
                        cur.execute(insert_query)
                        msg = f"Insert new active due date for task id: {task_id}"
                    conn.commit()
                return msg
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error
    
def prep_insert_due_date_queries(task_id: int, due_date: str) -> Tuple[str, str, str, str]:
    """
    Prepare SQL queries for inserting/updating due dates.

    Args:
        task_id (int): The ID of the task.
        due_date (str): The due date of the task.

    Returns:
        tuple: A tuple containing the following SQL queries:
            - select_query (str): The SELECT query for retrieving the existing due date for the task.
            - update_deactivate_query (str): The UPDATE query for deactivating the existing due date for the task.
            - update_activate_query (str): The UPDATE query for activating a new due date for the task.
            - insert_query (str): The INSERT query for inserting a new due date for the task.
    """
    select_query_base = 'SELECT * FROM app."Due_by" WHERE task_id = {0}'
    select_query = sql.SQL(select_query_base).format(sql.Literal(task_id))
    update_deactivate_query_base = 'UPDATE app."Due_by" SET is_active = false WHERE task_id = {0} AND is_active = true'
    update_activate_query_base = 'UPDATE app."Due_by" SET is_active = true WHERE task_id = {0} AND due_date = {1}'
    update_deactivate_query = sql.SQL(update_deactivate_query_base).format(sql.Literal(task_id))
    update_activate_query = sql.SQL(update_activate_query_base).format(sql.Literal(task_id), sql.Literal(due_date))
    insert_query_base = 'INSERT INTO app."Due_by" (task_id, due_date, is_active) VALUES ({0}, {1}, true)'
    insert_query = sql.SQL(insert_query_base).format(sql.Literal(task_id), sql.Literal(due_date))
    return select_query, update_deactivate_query, update_activate_query, insert_query

def check_current_due_date(cur: psycopg2.extensions.cursor, due_date_rows: list, due_date: str,
                            update_deactivate_query: str) -> tuple:
    """
    Check the current due date and perform necessary modifications.

    Args:
        cur (psycopg2.extensions.cursor): The database cursor object.
        due_date_rows (list): A list of dictionaries representing the rows of due dates.
        due_date (str): The new due date to be checked.
        update_deactivate_query (str): The SQL query to deactivate the previous old due date.

    Returns:
        tuple: A tuple containing the following values:
            - modification_necessary (bool): Indicates whether modification is necessary.
            - due_date_already_present (bool): Indicates whether the due date is already present.
            - msg (str): A message indicating the result of the operation.
    """
    modification_necessary = True
    due_date_already_present = False
    active_due_date = None
    for row in due_date_rows:
        if row["is_active"]:
            active_due_date = row["due_date"]
        if str(row["due_date"]) == due_date:
            due_date_already_present = True
    # If the new due date is different from the active one, update the active row
    if str(active_due_date) != due_date:
        cur.execute(update_deactivate_query) # Deactivate previous old due date
        msg: str = "Updated active due date"
    else:
        modification_necessary = False
        msg = "New due date is the same as the active one"
    return modification_necessary, due_date_already_present, msg
