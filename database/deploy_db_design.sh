#!/bin/bash

handle_error() {
    echo "An error occurred on line $1"
    exit 1
}

trap 'handle_error $LINENO' ERR

# Gets location of this script and uses it as a base
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

echo Deploying Database design

docker cp $SCRIPTPATH/simple-app-db-v1.0.sql vitualization-level-1-prototype-app-db-1:/tmp;

command_output=$(docker exec vitualization-level-1-prototype-app-db-1 psql -U postgres -a -f /tmp/simple-app-db-v1.0.sql | tr -d '\r');

if [[ $command_output == *"ROLLBACK"* ]]; then 
  echo "Could not deploy the design, is the DB already configured?"
  exit 1 
else 
  echo "Database design successfully deployed" 
  exit 0 
fi
