Write-Host "====== Activating virtual environment ======"
.\.venv\Scripts\activate

# Write-Host "====== Initializing database ======"
# flask --app app.web init-db

Start-Sleep -Seconds 10

Write-Host "====== Setup is ready ======"

# Start File Upload Server
Start-Process powershell -ArgumentList "-NoExit","-Command","Write-Host 'Starting file upload server..'; cd local-do-files; python app.py"

Start-Sleep -Seconds 10

# Start worker process
Start-Process powershell -ArgumentList "-NoExit","-Command","Write-Host 'Starting worker process..'; .\.venv\Scripts\activate; inv devworker"

Start-Sleep -Seconds 10

Write-Host "====== Starting Python Server ======"
inv dev


Write-Host "==== Ending script execution ===="