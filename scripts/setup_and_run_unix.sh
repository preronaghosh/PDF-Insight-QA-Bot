#!/bin/bash

echo "====== Starting initial setup ======"

# Create a virtual environment
echo "====== Creating virtual environment ======"
python3 -m venv .venv

# Activate virtual environment
echo "====== Activating virtual environment ======"
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
echo "====== Initializing database ======"
flask --app app.web init-db

sleep 10

echo "====== Completed setup ======"

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
