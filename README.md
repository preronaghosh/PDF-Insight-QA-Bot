# First Time Setup

```
# Create a virtual environment
python -m venv .venv

# On MacOS, WSL, Linux
source .venv/bin/activate

# On Windows
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask --app app.web init-db
```

# Running the app

There are three separate processes that need to be running for the app to work: the server, the worker, and Redis.

If you stop any of these processes, you will need to start them back up!

Commands to start each are listed below. If you need to stop them, select the terminal window the process is running in and press Control-C

### To run the Python server

```
inv dev
```

### To run the worker

```
# For native windows platform, run the following command
pip install gevent

# For MacOS, WSL, Linux, remove '-P gevent' flag from tasks.py (line: 17)
inv devworker
```

### To run Redis (Not required on native Windows, use redis.com)

```
redis-server
```

### To reset the database

```
flask --app app.web init-db
```

### To run file upload server locally

```
cd local-do-files/

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py

# Update your own .env file with the following line:
UPLOAD_URL=http://localhost:8050
```

# Scripts

### Before executing the following commands, place the required script into root directory 'pdf-insight-qa-bot/'.

Native Windows OS:


```
# Deactivate virtual env if activated and remove .\.venv (if any exists)

deactivate
Remove-Item .venv (Type Y when prompted)

# Initial setup and running all the three processes  
.\setup_and_run_windows.ps1

# For consecutive runs using existing virtual env:
.\run_windows.ps1
```

Unix-based OS/WSL:

```
# Deactivate virtual env if activated and remove .\.venv (if any exists)

deactivate
rm -rf .venv

# Initial setup and running all the three processes
chmod +x setup_and_run_unix.sh   
./setup_and_run_unix.sh

# For consecutive runs using existing virtual env:
chmod +x run_unix.sh
./run_unix.sh
```
