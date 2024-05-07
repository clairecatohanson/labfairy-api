#!/bin/bash

rm db.sqlite3
rm -rf ./labfairyapi/migrations
python3 manage.py makemigrations labfairyapi
python3 manage.py migrate
python3 manage.py migrate labfairyapi
python3 manage.py loaddata user token building room location maintenance equipment equipment_maintenance lab lab_equipment researcher consumable inventory lab_inventory consumable_inventory

