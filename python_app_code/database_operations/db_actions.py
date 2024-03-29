from database_operations import db_config as dbc
from datetime import datetime
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from typing import Optional, Tuple
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

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

def compose_task_insert_update_values(task_name: str, task_descrip: str, creation_date: str, task_status: str) -> tuple:
    """
    Composes the column names and values for inserting or updating a task in the database.

    Args:
        task_name (str): The name of the task.
        task_descrip (str): The description of the task.
        creation_date (str): The creation date of the task.
        task_status (str): The status of the task.

    Returns:
        tuple: A tuple containing two tuples - the first tuple contains the column names, and the second tuple contains the corresponding values.

    Raises:
        ValueError: If no values are provided for insertion or update.
    """
    column_names = []
    values = []
    if (task_name is not None):
        column_names.append("task_name")
        values.append(task_name)
    if (task_descrip is not None):
        column_names.append('task_descrip')
        values.append(task_descrip)
    
    if (creation_date is not None):
        column_names.append('creation_date')
        values.append(creation_date)
    
    if (task_status is not None):
        column_names.append('task_status')
        values.append(task_status)
    
    if len(column_names) == 0:
        raise ValueError("No values to insert or update")
    
    return (tuple(column_names), tuple(values))


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
    str = compose_task_insert_update_values(task_name, task_descrip, creation_date, task_status)

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
                insert_due_date(conn, new_id, due_date)
            
            return new_id
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
    str = compose_task_insert_update_values(task_name, task_descrip, task_creation_date, task_status)
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
                    insert_into_due_by_table(task_id, due_date)

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