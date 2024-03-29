from flask import request, Blueprint, jsonify
import re
from database_operations import db_actions as dba
from rest_api import api_operations_utils as aou

due_by_api = Blueprint('due_by_api', __name__)
utils = aou.api_operations_utils()

@due_by_api.route('/tasks/<task_id>/due-by', methods=['GET', 'POST', 'PUT'])
def list_due_by_route(task_id: int) -> jsonify:
   """
   Route handler for listing due dates and performing CRUD operations on due dates.

   Args:
      task_id (int): The ID of the task.

   Returns:
      jsonify: The response containing the due dates or an error message.
   """
   if not utils.is_task_id_valid(task_id):
      return jsonify({'error': 'Parameter "task-id" in "/tasks/<task-id>/due-by" must be a valid integer.'}), 400
   if request.method == 'GET':
      return get_task_due_dates(task_id)
   elif request.method == "POST":
      return post_due_date(task_id, request)
   elif request.method == "PUT":
      return put_due_date(task_id, request)
   
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
         tmp = utils.validate_due_date_json(received_request)
         if tmp[1] == 200:
            parsed_req = utils.parse_received_request(received_request.get_json())
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