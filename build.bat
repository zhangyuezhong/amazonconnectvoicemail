
powershell if (Test-Path package) { Remove-Item -Recurse -Force package; }
powershell New-Item package -itemType Directory
pip3 install --target ./package -r requirements.txt --no-user
powershell Remove-Item package\*.dist-info -Recurse
powershell Copy-Item src\* -Destination package -Recurse -Exclude __pycache__

