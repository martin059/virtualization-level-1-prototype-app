from database_operations import db_config as dbc, db_due_by_actions as dbdba
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# This script defines all operations that can be done on the Task table

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
                dbdba.insert_due_date(conn, new_id, due_date)
            
            return new_id
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
                    dbdba.insert_into_due_by_table(task_id, due_date)

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