from database_operations import db_config as dbc
from datetime import datetime
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

def connect(config = None):
    if config is None:
        config = dbc.load_config()

    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return None

def get_today_date(format = '%Y-%m-%d'):
    # The default format matches the postgreSQL DATE standard
    # An example of the default return is: '2024-03-03'
    return datetime.today().strftime(format)

def get_all_tasks():
    """ Retrieve all data from the Tasks table """

    select_query = 'SELECT * FROM app."Task" ORDER BY id ASC'
    config  = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(select_query)
                return cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    
def get_a_task(task_id: str):
    """ Retrieve one task from the Tasks table """

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
        return None
    
def get_due_by(task_id: str):
    """ Retrieve all due dates of a given task from the Due_by table """

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
        return None

def compose_task_insert_update_values(task_name, task_descrip, creation_date, task_status):
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


def insert_into_task_table(task_name, task_descrip = None, creation_date = None, task_status = None, due_date = None):
    """ A new task in the database, if successful returns new tasks id from the DB"""

    # TODO maybe add some error catching in here so that the DB doens't do it?
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
            if (due_date is not None):
                insert_due_date(conn, new_id, due_date)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return new_id

def insert_due_date(conn, task_id, due_date):
    # First version of this function won't take into account to update the due date if there was one before, it just inserts it.

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
        return error

def update_task(task_id: str, task_name = None, task_descrip = None, task_creation_date = None, task_status = None, due_date = None):
    """ Updates the data of a Task """

    # TODO due_date functionality must be added later
    update_query_base = 'UPDATE app."Task" SET {0} WHERE id = {1}'
    str = compose_task_insert_update_values(task_name, task_descrip, task_creation_date, task_status)
    update_query = sql.SQL(update_query_base).format(
                        sql.SQL(',').join(map(lambda x: sql.SQL('{0} = {1}').format(sql.Identifier(x[0]), sql.Literal(x[1])), zip(str[0], str[1]))),
                        sql.Literal(task_id)
                    )
    config  = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            # return update_query.as_string(conn) # DEBUG
            with conn.cursor() as cur:
                cur.execute(update_query)
                conn.commit()
                return None

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error

def delete_task(task_id: str):
    """ Updates the state of a Task to be 'DELETED' """

    update_query_base = 'UPDATE app."Task" SET task_status = \'Deleted\' WHERE id = {0}'
    update_query = sql.SQL(update_query_base).format(sql.Literal(task_id))
    config  = dbc.load_config()
    try:
        with psycopg2.connect(**config) as conn:
            print(update_query.as_string(conn))
            with conn.cursor() as cur:
                cur.execute(update_query)
                conn.commit()
                return None

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error
    
# TODO CHECK IT IF IT WORKS AS EXPECTED !!!!!!!!!!
def insert_into_due_by_table(task_id, due_date):
    """ Insert or update a due date for a task in the Due_by table """
    select_query_base = 'SELECT * FROM app."Due_by" WHERE task_id = {0}'
    select_query = sql.SQL(select_query_base).format(sql.Literal(task_id))
    update_deactivate_query_base = 'UPDATE app."Due_by" SET is_active = false WHERE task_id = {0} AND is_active = true'
    update_activate_query_base = 'UPDATE app."Due_by" SET is_active = true WHERE task_id = {0} AND due_date = {1}'
    update_deactivate_query = sql.SQL(update_deactivate_query_base).format(sql.Literal(task_id))
    update_activate_query = sql.SQL(update_activate_query_base).format(sql.Literal(task_id), sql.Literal(due_date))
    insert_query_base = 'INSERT INTO app."Due_by" (task_id, due_date, is_active) VALUES ({0}, {1}, true)'
    insert_query = sql.SQL(insert_query_base).format(sql.Literal(task_id), sql.Literal(due_date))
    config = dbc.load_config()
    msg = None
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Check if the task has an active due date
                cur.execute(select_query)
                rows = cur.fetchall()
                update_necessary = True
                due_date_already_present = False
                if rows:
                    active_due_date = None
                    for row in rows:
                        if row["is_active"]:
                            active_due_date = row["due_date"]
                        if row["due_date"] == due_date:
                            due_date_already_present = True
                    # If the new due date is different from the active one, update the active row
                    if active_due_date != due_date:
                        cur.execute(update_deactivate_query) # Deactivate previous old due date
                        msg = "Updated active due date"
                    else:
                        update_necessary = False
                        msg = "New due date is the same as the active one"
                # If update is necessary, and due date is already present, activate row
                if update_necessary:
                    if due_date_already_present:
                        cur.execute(update_activate_query)
                        msg = f"Updated active due date for task id: {task_id}"
                    # If update is necessary, and new due date is not present, insert a new row
                    else:
                        cur.execute(insert_query)
                        msg = f"Insert new active due date for task id: {task_id}"
                    conn.commit()
                return msg
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error

# The following two operations are for debugging since they print directly their results to the console
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