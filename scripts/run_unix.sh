#!/bin/bash

echo "====== Activating virtual environment ======"
source .venv/bin/activate

sleep 10

Write-Host "====== Setup is ready ======"

# Start File Upload Server
echo "Starting file upload server.."
cd local-do-files
pip install -r requirements.txt
python app.py &

sleep 10

# Start worker process
echo "Starting worker process using celery.."
source .venv/bin/activate
pip install gevent
inv devworker &

sleep 10

# Start redis server
echo "Starting Redis server as a Message Worker" 
redis-server &

sleep 10

echo "====== Starting Python Server ======"
inv dev

echo "==== Ending script execution ===="