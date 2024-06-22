# First Virtualization level: Sample App

This project contains the required code for deploying and running the sample development app.

This project deploys and runs a simple dockerized web app that illustrates the main use case of the main project, which is to deploy a fully ready development environment with as few user actions as possible under diverse software environments without sacrificing flexibility and consistency.

## Sample App

The app itself is a simple web app that tracks To-Do tasks. It is a containerized web app running on three containers:

- **Postgres Container**: It contains the SQL database which stores all information for the app.
- **Python Container**: It serves as the Back End (BE) for the app using Python and Flask to expose a REST API.
- **Svelte Container**: It serves as the Front End (FE) for the app using Svelte, TypeScript, and Sveltestrap.

All three containers are running the latest official stable release on Alpine Linux. Unless specifically stated otherwise, all versions used are the _current stable release_ at the time of compilation.

To compile and run the app, read the [To run the app](#to-run-the-app) section.

To run the automatic tests, read the [Testing](#testing) section.

### General principle

As previously stated, this is a simple app that keeps track of To-Do tasks that are stored in a SQL database whose design is represented in [this entity-relationship diagram](database/simple-app-erd.png).

A Task has the following elements:

- `Id`: The Task's numerical ID, automatically assigned by the database upon creation. It is a positive number starting at 1 and increasing sequentially.
- `Task Name`: The Task's name given by the user. All Tasks must have a name.
- `Task Description`: The Task's description given by the user.
- `Creation Date`: The Task's creation date which is automatically assigned by the database upon creation.
- `Task Status`: The Task's current status which can only be one of the following:
  - `Created`: The default state of a Task. It indicates that a Task has been created and is pending.
  - `Done`: It indicates that a Task has been completed.
  - `Dropped`: It indicates that a Task has been dropped without being completed.
  - `Deleted`: It indicates that a Task has been deleted.
  - `Postponed`: It indicates that a Task has been postponed.

A task can optionally have one or more due dates associated with it, but a Task can have, at most, one due date active at any given time.

This app does not allow a user to literally delete a Task from the database unless the user sends the SQL query directly to the database. Instead, the user can only mark it as "Deleted".

The communication between the FE app and the BE app is done through REST requests. The communication between the BE app and the database is done through the `psycopg2` library. All communication between the database and the FE app must go through the BE app.

### To run the app

1. Clone the repository (`git clone git@github.com:martin059/virtualization-level-1-prototype-app.git`)
2. Change directory to the front-end service (`cd virtualization-level-1-prototype-app/svelte_app_code/virtualization-level-1-prototype-app-svelte/`)
3. Get the initial build for the front-end service that the service will later require while building the image (`npm install`)
4. Go back to the main directory (`cd ../..` or `cd <path_to_cloned_repo>/virtualization-level-1-prototype-app`)
5. Raise the docker containers (`docker-compose up -d`)
6. Execute deploy bash script to set up database structure (`bash database/deploy_db_design.sh` or `bash <path_to_cloned_repo>/database/deploy_db_design.sh`)
7. Open the browser and go to http://127.0.0.1:5002 to access the Front-end app.

## Testing

### To test the Python API directly with Postman collection

1. Import [Postman collection](https://github.com/martin059/virtualization-level-1-prototype-app/blob/master/postman_testing_requests/testing-postman-collection.json)
2. Set the `baseUrl` collection's variable to `http://127.0.0.1:5001` (the collection has these values pre-configured).
3. Run the collection's test **sequentially** from top to bottom (otherwise, some tests will fail as a required entry wasn't previously inserted).

### To test the Python and Database integration

No automatic tool has been used for this part to avoid adding complexity to it. It requires manual launching of the tests and manual validation of results. However, the functionality tested is simple, so if no error messages are thrown it can be assumed that it is working as expected.

1. If it is commented, uncomment [this line](https://github.com/martin059/virtualization-level-1-prototype-app/blob/master/python_app_code/app.py#L28).
2. Make sure that the script `deploy_db_design.sh` has been executed previously, otherwise it will fail since the DB isn't configured.
3. Execute `docker exec virtualization-level-1-prototype-app-python-1 python3 app.py` and debug manually.
