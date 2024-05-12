# First Virtualization level: Sample App

This project contains the required code for deploying and running the sample development app.

This projects deploys and runs a simple dockerized web app that illustrates the main use case of the main project which is to deploy a fully ready development environment with as few user-actions as possible under diverse software environments without sacrificing flexibility and consistency to achieve it.

## Sample App

The app itself is a simple web app that is made to run on set of docker containers.

### To run the app

1. Clone the repository (`git clone <url>`)
2. Change directory to the front-end service (`cd virtualization-level-1-prototype-app/svelte_app_code/virtualization-level-1-prototype-app-svelte/`)
3. Get initial build for the front-end service that the service will later require while building the image (`npm install`)
4. Go back to the main directory (`cd ../..` or `cd <path_to_cloned_repo>/virtualization-level-1-prototype-app`)
5. Raise the docker containers (`docker-compose up -d`)
6. Execute deploy bash script to set up database structure (`bash <path_to_cloned_repo>/database/deploy_db_design.sh`)

## Testing

### To test the Python API directly with postman collection

1. Import [postman collection](https://github.com/martin059/virtualization-level-1-prototype-app/blob/master/postman_testing_requests/testing-postman-collection.json)
2. Set the `baseUrl` collection's variable to `http://127.0.0.1:5001`
3. Run the collection's test **sequentially** from top to bottom (otherwise, some tests will fail as a required entry wasn't previously inserted)

### To test the Python and Database integration

No automatic tool has been used for this part to avoid adding complexity to it. It requires manual launching of the tests and manual validation of results. However, the functionality tested is simple, so if no error messages are thrown it can be assumed that it is working as expected.

1. If it is commented, uncomment [this line](https://github.com/martin059/virtualization-level-1-prototype-app/blob/master/python_app_code/app.py#L17).
2. Make sure that the script `deploy_db_design.sh` has been executed previously, otherwise it will fail since the DB isn't configured.
3. Execute `docker exec virtualization-level-1-prototype-app-python-1 python3 app.py` and debug manually.