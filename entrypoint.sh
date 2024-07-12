#!/bin/bash

cd /app
pip install --no-cache-dir -r requirements.txt
apt-get update && apt-get install -y sqlite3 libsqlite3-dev
#python /app/app.py
python -m flask run --host 0.0.0.0 --port 5000