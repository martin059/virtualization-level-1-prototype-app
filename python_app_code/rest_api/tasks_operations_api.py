from flask import request, Blueprint, jsonify
import re
from database_operations import db_actions as dba
from rest_api import api_operations_utils as aou

tasks_api = Blueprint('tasks_api', __name__)

@tasks_api.route('/tasks', methods=['GET', 'POST'])
@tasks_api.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def list_tasks_route(task_id: int = None) -> jsonify:
   """
   Route handler for listing tasks and performing CRUD operations on tasks.

   Args:
      task_id (int, optional): The ID of the task. Defaults to None.

   Returns:
      JSON response: The response containing the result of the operation or an error message.
   """
   if task_id is not None:
      if not aou.is_task_id_valid(task_id):
         return jsonify({'error': 'Parameter "task-id" in "/tasks/<task-id>" must be a valid integer.'}), 400
      
   if request.method == 'GET':
      if task_id is None:
         return list_tasks()
      else:
         return get_task(task_id)
   elif request.method == "POST":
      return add_task(request)
   elif request.method == "DELETE":
      if task_id is None:
         return jsonify({'error': 'Parameter "task-id" in "/tasks/<task-id>/" must be given to delete a task.'}), 400
      else:
         return delete_task(task_id)
   elif request.method == "PUT":
      if task_id is None:
         return jsonify({'error': 'Parameter "task-id" in "/tasks/<task-id>/" must be given to update a task.'}), 400
      else:
         return update_task(task_id, request)
   
@tasks_api.route('/tasks/<task_id>/due-by', methods=['GET', 'POST', 'PUT'])
def list_due_by_route(task_id: int) -> jsonify:
   """
   Route handler for listing due dates and performing CRUD operations on due dates.

   Args:
      task_id (int): The ID of the task.

   Returns:
      jsonify: The response containing the due dates or an error message.
   """
   if not aou.is_task_id_valid(task_id):
      return jsonify({'error': 'Parameter "task-id" in "/tasks/<task-id>/due-by" must be a valid integer.'}), 400
   if request.method == 'GET':
      return get_task_due_dates(task_id)
   elif request.method == "POST":
      return post_due_date(task_id, request)
   elif request.method == "PUT":
      return put_due_date(task_id, request)
   
def list_tasks() -> jsonify:
   """
   Retrieves a list of all tasks from the database.

   Returns:
      jsonify: A list of tasks.
   """
   try:
      return dba.get_all_tasks()
   except Exception as e:
      return jsonify({'error': str(e)}), 500

def get_task(id: str) -> jsonify:
   """
   Retrieve a task by its ID.

   Args:
       id (str): The ID of the task to retrieve.

   Returns:
       If the task is found, the task details are returned.
       If the task is not found, a JSON response with an error message and status code 404 is returned.
       If an exception occurs during the retrieval process, a JSON response with the error message and status code 500 is returned.
   """
   try:
      db_response = dba.get_a_task(id)
      if db_response is None or len(db_response) == 0:
         return jsonify({'error': 'Task with id {} not found'.format(id)}), 404
      else:
         return db_response
   except Exception as e:
      return jsonify({'error': str(e)}), 500
   
def get_task_due_dates(id: str) -> jsonify:
   """
   Retrieves the due dates for a task with the given ID.

   Parameters:
   - id (str): The ID of the task.

   Returns:
   - If the task's due dates are found in the database, the function returns the response from the database.
   - If the task's due dates are not found, the function returns a JSON response with an error message and a 404 status code.
   - If an exception occurs during the database operation, the function returns a JSON response with the error message and a 500 status code.
   """
   id = int(id)
   try:
      db_response = dba.get_due_by(id)
      if db_response is None or len(db_response) == 0:
         return jsonify({'error': 'Task\'s due date with task\'s id {} not found'.format(id)}), 404
      else:
         return db_response
   except Exception as e:
      return jsonify({'error': str(e)}), 500
   

def add_task(received_request: request) -> jsonify:
   """
   Adds a new task to the task table.

   Args:
      received_request (request): The request object containing the task details.

   Returns:
      A JSON response containing the new task ID if successful, or an error message if unsuccessful.
   """
   tmp = aou.validate_json(received_request)
   if tmp[1] == 200:
      new_task = aou.parse_received_request(received_request.get_json())
      if new_task["due_date"] is not None:
         if not aou.validate_due_date_json(received_request):
            return jsonify({"error": "A Due Date must have a valid 'due_date' with the 'YYYY-MM-DD' format."}), 400
      try:
         response = dba.insert_into_task_table(new_task["task_name"], new_task["task_descrip"], 
                              new_task["creation_date"], new_task["task_status"], new_task["due_date"])
         return jsonify({"new_task_id": response}), 201
      except Exception as e:
         return jsonify({'error': str(e)}), 500
     
   else:
      return tmp[0], tmp[1]

def post_due_date(task_id: int, received_request: request, comming_from_put: bool = False) -> jsonify:
   """
   If invoked form POST method, creates a new due date for a task.
   If invoked from PUT method, updates the due date for a task.
   This method makes the distinction between the two cases to enforce the correct behavior of a REST API.

   Args:
      task_id (int): The ID of the task.
      received_request (request): The request object containing the due date information.
      comming_from_put (bool, optional): If True, the function is invoked from the PUT method. Defaults to False.

   Returns:
      jsonify: A JSON response containing the result of the operation with the following status codes:
         404: If the task with the given ID is not found, or if the due date doesn't exist for the task and comming from PUT.
         409: If a due date already exists for the task and if comming from POST.
         500: If an unexpected error occurs.
   """
   id = int(task_id)
   try:
      task = dba.get_a_task(id)
      if task is None or len(task) == 0:
         return jsonify({'error': 'Task with id {} not found, create a task beforehand'.format(id)}), 404
      else:
         tmp = aou.validate_due_date_json(received_request)
         if tmp[1] == 200:
            parsed_req = aou.parse_received_request(received_request.get_json())
            check_if_due_date_exists = dba.get_specific_due_by(id, parsed_req["due_date"])
            if not comming_from_put:
               if check_if_due_date_exists is not None and len(check_if_due_date_exists) > 0:
                  return jsonify({"error": "Due date already exists for this task, use PUT method instead to update it."}), 409
            else: 
               if check_if_due_date_exists is None or len(check_if_due_date_exists) == 0:
                  return jsonify({"error": "Due date doesn't exists for this task, use POST method instead to create it."}), 404
            response = dba.insert_into_due_by_table(id, parsed_req["due_date"])
            return jsonify({"message": response}), 200 if comming_from_put else 201
         else:
            return tmp[0], tmp[1]
   except Exception as e:
      return jsonify({'error': str(e)}), 500
      
def put_due_date(task_id: int, received_request: request) -> jsonify:
   """
   Updates the due date of a task with the given task_id.

   Args:
      task_id (int): The ID of the task to update.
      received_request (request): The request object containing the new due date.

   Returns:
      jsonify: The JSON response indicating the success or failure of the operation.
   """
   return post_due_date(task_id, received_request, True)

def update_task(task_id: int, received_request: request) -> jsonify:
   """
   Update a task with the given task_id using the information provided in the received_request.

   Args:
      task_id (int): The ID of the task to be updated.
      received_request (request): The request object containing the updated task information.

   Returns:
      jsonify: A JSON response containing the updated task information or an error message.

   """
   id = int(task_id)
   try:
      task = dba.get_a_task(id)
      if task is None or len(task) == 0:
         return jsonify({'error': 'Task with id {} not found'.format(id)}), 404
      else:
         tmp = aou.validate_json(received_request, False)
         if tmp[1] == 200:
            update_task = aou.parse_received_request(received_request.get_json())
            if update_task["due_date"] is not None:
               if not aou.validate_due_date_json(received_request):
                  return jsonify({"error": "A Due Date must have a valid 'due_date' with the 'YYYY-MM-DD' format."}), 400
            response = dba.update_task(id, update_task["task_name"], update_task["task_descrip"], 
                                 update_task["creation_date"], update_task["task_status"], update_task["due_date"])
            if response is None:
               return '', 204
            else:
               return jsonify({"error": str(response)}), 400
         else:
            return tmp[0], tmp[1]
   except Exception as e:
      return jsonify({'error': str(e)}), 500

def delete_task(task_id: int) -> jsonify:
   """
   Changes the status of a task with the given task_id to 'Deleted'.

   Args:
      task_id (int): The ID of the task to be deleted.

   Returns:
      jsonify: A JSON response indicating the success or failure of the deletion.
   """
   try:
     task = dba.get_a_task(task_id)
     if task is None or len(task) == 0:
       return jsonify({'error': 'Task with id {} not found'.format(task_id)}), 404
     dba.delete_task(task_id)
     return '', 204
   except Exception as e:
     return jsonify({'error': str(e)}), 500
