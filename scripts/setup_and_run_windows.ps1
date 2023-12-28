Write-Host "====== Starting initial setup ======"

# Create a virtual environment
Write-Host "====== Creating virtual environment ======"
python -m venv .venv

# Activate virtual environment
Write-Host "====== Activating virtual environment ======"
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
Write-Host "====== Initializing database ======"
flask --app app.web init-db

Start-Sleep -Seconds 10

Write-Host "====== Completed setup ======"

# Start File Upload Server
Start-Process powershell -ArgumentList "-NoExit","-Command","Write-Host 'Starting file upload server..'; cd local-do-files; pip install -r requirements.txt; python app.py"

Start-Sleep -Seconds 10

# Start worker process
Start-Process powershell -ArgumentList "-NoExit","-Command","Write-Host 'Starting worker process using celery..'; .\.venv\Scripts\activate; pip install gevent; inv devworker"

Start-Sleep -Seconds 10

Write-Host "====== Starting Python Server ======"
inv dev


Write-Host "==== Ending script execution ===="