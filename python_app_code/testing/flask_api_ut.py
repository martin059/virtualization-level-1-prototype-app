# This File contains a series of Unit Tests (UTs) that treats the functionality of this code to expose a REST API
# as a single unit that will be tested. For simplicity, PyUnit wasn't implemented, but a postman collection is to be used
# instead.

from flask import request, Blueprint

basic_flask_api = Blueprint('basic_flask_api', __name__)

# Base how to build REST API: https://www.linode.com/docs/guides/create-restful-api-using-python-and-flask/

# The following is a simple structure to do some quick debugging of the REST API
in_memory_datastore = {
   "COBOL" : {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
   "ALGOL" : {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
   "APL" : {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
}

@basic_flask_api.get('/')
def hello_rest():
   return "Hello World from REST!"

@basic_flask_api.route('/programming_languages', methods=['GET', 'POST'])
def list_programming_languages_route():
   if request.method == 'GET':
      return list_programming_languages()
   elif request.method == "POST":
      return create_programming_language(request.get_json(force=True))
    
def list_programming_languages():
   return {"programming_languages":list(in_memory_datastore.values())}

@basic_flask_api.route('/programming_languages/<programming_language_name>',  methods=['GET', 'PUT', 'DELETE'])
def get_programming_language_route(programming_language_name):
   if request.method == 'GET':
       return get_programming_language(programming_language_name)
   elif request.method == "PUT":
      return update_programming_language(programming_language_name, request.get_json(force=True))
   elif request.method == "DELETE":
      return delete_programming_language(programming_language_name)
    
def get_programming_language(programming_language_name):
   return in_memory_datastore[programming_language_name]
   
def create_programming_language(new_lang):
   language_name = new_lang['name']
   in_memory_datastore[language_name] = new_lang
   return new_lang

def update_programming_language(lang_name, new_lang_attributes):
   lang_getting_update = in_memory_datastore[lang_name]
   lang_getting_update.update(new_lang_attributes)
   return lang_getting_update

def delete_programming_language(lang_name):
   deleting_lang = in_memory_datastore[lang_name]
   del in_memory_datastore[lang_name]
   return deleting_lang