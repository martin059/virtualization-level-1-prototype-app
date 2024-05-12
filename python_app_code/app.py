from flask import Flask
from flask_cors import CORS
from rest_api import tasks_operations_api
from rest_api import due_by_operations_api

# Imports for testing and debugging:
from testing import flask_api_ut
from testing import db_actions_it

#Declare Flask app
app = Flask(__name__)
app.register_blueprint(flask_api_ut.basic_flask_api)
app.register_blueprint(tasks_operations_api.tasks_api)
app.register_blueprint(due_by_operations_api.due_by_api)
CORS(app)


def main():
    print('Hello World!')


if __name__ == "__main__":
    main()
    
    # By running the following line, it will launch of Integration Tests between the python and postgres containers
    # do so with the following command: `docker exec virtualization-level-1-prototype-app-python-1 python3 app.py`
    # Otherwise, this app is meant to be launched and runs automatically with the raising of the docker container
    db_actions_it.initial_testing_console()
    