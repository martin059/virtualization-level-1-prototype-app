from flask import Flask
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


def main():
    print('Hello World!')


if __name__ == "__main__":
    main()
    
    # Uncomment the following line to enable launch of Integration Tests between python and postgres containers
    # db_actions_it.initial_testing_console()
    