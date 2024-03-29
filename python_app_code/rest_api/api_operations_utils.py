import re
from flask import request, jsonify

class api_operations_utils:
    """
    Utility class for API operations. Mostly used for validating and parsing of received requests.
    """

    @staticmethod
    def parse_received_request(received_request: dict) -> dict:
        """
        Parses the received request and extracts relevant information.

        Args:
            received_request (dict): The received request as a dictionary.

        Returns:
            dict: A dictionary containing the parsed information from the received request.
        """
        parsed_req = {}
        parsed_req["task_name"] = received_request.get("task_name") if isinstance(received_request, dict) else None
        parsed_req["task_descrip"] = received_request.get("task_descrip") if isinstance(received_request, dict) else None
        parsed_req["creation_date"] = received_request.get("creation_date") if isinstance(received_request, dict) else None
        parsed_req["task_status"] = received_request.get("task_status") if isinstance(received_request, dict) else None
        parsed_req["due_date"] = received_request.get("due_date") if isinstance(received_request, dict) else None
        return parsed_req
    
    @staticmethod
    def validate_json(received_request: request, needs_to_have_name: bool = True) -> jsonify:
       """
       Validates the JSON data in the received request.

       Args:
          received_request (request): The request object containing the JSON data.
          needs_to_have_name (bool, optional): Indicates whether the JSON data needs to have a 'task_name' field. Defaults to True.

       Returns:
          jsonify: A JSON response indicating the validation result.
       """
       if not received_request.json:  # Check if the request body is empty
          return jsonify({'error': 'Empty request body'}), 400

       if received_request.is_json:
          try:
             req = received_request.get_json()
             if not needs_to_have_name:
                return jsonify({"message": "Valid JSON received"}), 200
             elif aou.has_task_name(req):
                return jsonify({"message": "Valid JSON received"}), 200
             else:
                return jsonify({"error": "A new Task must have a 'task_name'."}), 400
          except Exception as e:
             return jsonify({"error": "Invalid JSON format", "details": str(e)}), 400
       else:
          return jsonify({"error": "Request does not contain JSON data"}), 400
    
    @staticmethod
    def has_valid_due_date(new_due_date_to_validate: dict) -> bool:
       """
       Checks if the JSON data has a field named "due_date" with a valid format.

       Args:
          new_due_date_to_validate (dict): The JSON data to validate.

       Returns:
          bool: True if the JSON data has a valid "due_date" field, False otherwise.
       """
       return ("due_date" in new_due_date_to_validate and 
            isinstance(new_due_date_to_validate["due_date"], str) and 
            re.match(r'^\d{4}-\d{2}-\d{2}$', new_due_date_to_validate["due_date"]))
    
    @staticmethod
    def validate_due_date_json(received_request: request) -> jsonify:
       """
       Validates the JSON data in the request body to ensure it contains a valid due date.

       Args:
          received_request (request): The request object containing the JSON data.

       Returns:
          jsonify: A JSON response indicating the result of the validation.
       """
       if not received_request.json:  # Check if the request body is empty
          return jsonify({'error': 'Empty request body'}), 400

       if received_request.is_json:
          try:
             req = received_request.get_json()
             if aou.has_valid_due_date(req):
                return jsonify({"message": "Valid JSON received"}), 200
             else:
                return jsonify({"error": "A new Due Date must have a valid 'due_date' with the 'YYYY-MM-DD' format."}), 400
          except Exception as e:
             return jsonify({"error": "Invalid JSON format", "details": str(e)}), 400
       else:
          return jsonify({"error": "Request does not contain JSON data"}), 400

    @staticmethod
    def is_task_id_valid(task_id: str) -> bool:
       """
       Check if the task_id is valid.

       Args:
          task_id (str): The task_id to be checked.

       Returns:
          bool: True if the task_id is an integer, False otherwise.
       """
       if task_id is None:
          return False
       if not isinstance(task_id, (int, float, str, bool)):
          return False
       return re.match(r'^-?\d+$', task_id)
   
    @staticmethod
    def has_task_name(new_task_to_validate: dict) -> bool:
       """
       Checks if the given JSON data contains a field named "task_name".

       Args:
          new_task_to_validate (dict): The JSON data to validate.

       Returns:
          bool: True if the JSON data has a field named "task_name", False otherwise.
       """
       if new_task_to_validate is None:
          return False
       return "task_name" in new_task_to_validate
