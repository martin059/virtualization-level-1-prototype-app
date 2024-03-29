# This File contains a series of Integration Tests (ITs) between the Python App and the postgres database.
# For simplicity, PyUnit wasn't implemented, only manual launching and validation of tests works.
from database_operations import db_actions as dba, db_task_actions as dbta

def initial_testing_console():
    print("I'll try to set up a connection with the db container:")
    dba.connect()
    print("\nI'll try to insert to example tasks")
    dbta.insert_into_task_table('1st task') # First task, only name
    dbta.insert_into_task_table('2nd task', 'This is the second one') # Second task, name and description
    dbta.insert_into_task_table('3rd task', 'This is the third one', task_status='Deleted') # Third task, name, description and status
    dbta.insert_into_task_table('4th task', creation_date='2024-03-01') # Fourth task, name and custom creation date
    dbta.insert_into_task_table('5th task', due_date='2024-03-17') # Fith task, name and due date
    print("I'll try to print them") # The due date of the 5th one won't appear
    dba.print_all_tasks()
    print("I'll try to print all task with due dates")
    dba.print_all_tasks_with_due_dates()
