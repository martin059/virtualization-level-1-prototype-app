from flask import request, Blueprint, jsonify
from database_operations import db_task_actions as dba
from rest_api import api_operations_utils as aou

# This script defines the REST API endpoints for the operations that can be done on the Task table

tasks_api = Blueprint('tasks_api', __name__)
utils = aou.api_operations_utils()

@tasks_api.route('/tasks', methods=['GET', 'POST'])
@tasks_api.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def list_tasks_route(task_id: int = None) -> jsonify:
   """
   Route handler for listing tasks and performing CRUD operations on tasks.

   Args:
      task_id (int, optional): The ID of the task. Defaults to None.

   Returns:
      JSON response: The response containing the result of the operation or an error message is a received parameter is invalid (400 code).
   """
   if task_id is not None:
      if not utils.is_task_id_valid(task_id):
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
   
def list_tasks() -> jsonify:
   """
   Retrieves a list of all tasks from the database.

   Returns:
      jsonify: A JSON response containing the result of the operation with the following status codes:
         200: If the tasks are found in the database, the function returns the response from the database.
         500: If an exception occurs during the database operation, the function returns an error message.
   """
   try:
      return jsonify(dba.get_all_tasks()), 200
   except Exception as e:
      return jsonify({'error': str(e)}), 500

def get_task(id: str) -> jsonify:
   """
   Retrieve a task by its ID.

   Args:
       id (str): The ID of the task to retrieve.

   Returns:
       jsonify: A JSON response containing the result of the operation with the following status codes:
         200: If the task is found in the database, the function returns the response from the database.
         404: If the task is not found, the function returns a not-found error message.
         500: If an exception occurs during the database operation, the function returns an error message.
   """
   try:
      db_response = dba.get_a_task(id)
      if db_response is None or len(db_response) == 0:
         return jsonify({'error': 'Task with id {} not found'.format(id)}), 404
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
      jsonify: A JSON response containing the result of the operation with the following status codes:
         201: If the task is successfully added to the database, the function returns the ID of the new task.
         400: If the task has an invalid format, the function returns an error message.
         500: If an exception occurs during the database operation, the function returns an error message.
   """
   tmp = utils.validate_json(received_request)
   if tmp[1] == 200:
      new_task = utils.parse_received_request(received_request.get_json())
      if new_task["due_date"] is not None:
         if not utils.validate_due_date_json(received_request):
            return jsonify({"error": "A Due Date must have a valid 'due_date' with the 'YYYY-MM-DD' format."}), 400
      try:
         response = dba.insert_into_task_table(new_task["task_name"], new_task["task_descrip"], 
                              new_task["creation_date"], new_task["task_status"], new_task["due_date"])
         return jsonify({"new_task_id": response}), 201
      except Exception as e:
         return jsonify({'error': str(e)}), 500
     
   else:
      return tmp[0], tmp[1]

def update_task(task_id: int, received_request: request) -> jsonify:
   """
   Update a task with the given task_id using the information provided in the received_request.

   Args:
      task_id (int): The ID of the task to be updated.
      received_request (request): The request object containing the updated task information.

   Returns:
      jsonify: A JSON response containing the result of the operation with the following status codes:
         204: If the task is successfully updated, the function returns an empty response.
         400: If the task has an invalid format, the function returns an error message.
         404: If the task is not found, the function returns a not-found error message.
         500: If an exception occurs during the database operation, the function returns an error message.

   """
   id = int(task_id)
   try:
      task = dba.get_a_task(id)
      if task is None or len(task) == 0:
         return jsonify({'error': 'Task with id {} not found'.format(id)}), 404
      else:
         tmp = utils.validate_json(received_request, False)
         if tmp[1] == 200:
            update_task = utils.parse_received_request(received_request.get_json())
            if update_task["due_date"] is not None:
               if not utils.validate_due_date_json(received_request):
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
      jsonify: A JSON response containing the result of the operation with the following status codes:
         204: If the task is successfully updated, the function returns an empty response.
         404: If the task is not found, the function returns a not-found error message.
         500: If an exception occurs during the database operation, the function returns an error message.
   """
   try:
     task = dba.get_a_task(task_id)
     if task is None or len(task) == 0:
       return jsonify({'error': 'Task with id {} not found'.format(task_id)}), 404
     dba.delete_task(task_id)
     return '', 204
   except Exception as e:
     return jsonify({'error': str(e)}), 500
