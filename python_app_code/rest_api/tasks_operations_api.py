from database_operations import db_actions as dba
from flask import request, Blueprint, jsonify
import re

tasks_api = Blueprint('tasks_api', __name__)

@tasks_api.route('/tasks', methods=['GET', 'POST'])
@tasks_api.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def list_tasks_route(task_id = None):
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
   
@tasks_api.route('/tasks/<task_id>/due-by', methods=['GET', 'POST'])
def list_due_by_route(task_id):
   if request.method == 'GET':
      if task_id is None:
         return jsonify({'error': 'Parameter "task-id" in "/tasks/<task-id>/due-by" must be given to get a task\'s due date.'}), 400 
      else:
         return get_task_due_dates(task_id)
   elif request.method == "POST":
      return "NOT YET DONE"
   
def list_tasks():
   return dba.get_all_tasks()

def get_task(id: str):
   try:
      id = int(id)
      db_response = dba.get_a_task(id)
      if db_response is None or len(db_response) == 0:
         return jsonify({'error': 'Task with id {} not found'.format(id)}), 404
      else:
         return db_response
   except ValueError:
      return jsonify({'error': 'Parameter "id" in "/tasks/<id>" must be an integer.'}), 400
   
def get_task_due_dates(id: str):
   try:
      id = int(id)
      db_response = dba.get_due_by(id)
      if db_response is None or len(db_response) == 0:
         return jsonify({'error': 'Task\'s due date with task\'s id {} not found'.format(id)}), 404
      else:
         return db_response
   except ValueError:
      return jsonify({'error': 'Parameter "task-id" in "/tasks/<task-id>/due-by" must be an integer.'}), 400 
   

def add_task(received_request: request):
   #The code won't validate if the creation_date or the due_date have a valid format
   tmp = validate_json(received_request)
   if tmp[1] == 200:
      new_task = parse_new_task_request(received_request.get_json())
      new_task_id = dba.insert_into_task_table(new_task["task_name"], new_task["task_descrip"], 
                                 new_task["creation_date"], new_task["task_status"], new_task["due_date"])
      return jsonify({"new_task_id": new_task_id}), 201
   else:
      return tmp[0], tmp[1]
   
def update_task(task_id, received_request: request):
   id = int(task_id)
   task = dba.get_a_task(id)
   if task is None or len(task) == 0:
      return jsonify({'error': 'Task with id {} not found'.format(id)}), 404
   else:
      tmp = validate_json(received_request)
      if tmp[1] == 200:
         update_task = parse_new_task_request(received_request.get_json())
         response = dba.update_task(id, update_task["task_name"], update_task["task_descrip"], 
                                    update_task["creation_date"], update_task["task_status"], update_task["due_date"])
         if response is None:
            return '', 204
         else:
            return jsonify({"error": str(response)}), 400
      else:
         return tmp[0], tmp[1]

def delete_task(task_id):
   response = dba.delete_task(task_id)
   if response is None:
      return '', 204
   else:
      return jsonify({"error": str(response)}), 400
      
    
def validate_json(received_request: request):
   if not received_request.json:  # Check if the request body is empty
       return jsonify({'error': 'Empty request body'}), 400
   
   if received_request.is_json:
       try:
           req = received_request.get_json()
           if has_task_name(req):
              return jsonify({"message": "Valid JSON received"}), 200
           else:
              return jsonify({"error": "A new Task must have a 'task_name'."}), 400
       except Exception as e:
           return jsonify({"error": "Invalid JSON format", "details": str(e)}), 400
   else:
       return jsonify({"error": "Request does not contain JSON data"}), 400

def has_task_name(new_task_to_validate: dict):
   # Returns True if the JSON data has a field named "task_name", False otherwise.
   return "task_name" in new_task_to_validate

def parse_new_task_request(received_request: dict):
   parsed_req = {}
   parsed_req["task_name"] = received_request["task_name"]
   parsed_req["task_descrip"] = received_request.get("task_descrip") if isinstance(received_request, dict) else None
   parsed_req["creation_date"] = received_request.get("creation_date") if isinstance(received_request, dict) else None
   parsed_req["task_status"] = received_request.get("task_status") if isinstance(received_request, dict) else None
   parsed_req["due_date"] = received_request.get("due_date") if isinstance(received_request, dict) else None
   return parsed_req
