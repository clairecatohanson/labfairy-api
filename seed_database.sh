#!/bin/bash

rm db.sqlite3
rm -rf ./labfairyapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations labfairyapi
python3 manage.py migrate labfairyapi
python3 manage.py loaddata building room location maintenance equipment equipmentmaintenance lab labequipment

