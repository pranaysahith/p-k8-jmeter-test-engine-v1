# ICAP+JMeter Dockerfile

## Deploy and run from within the PowerShell
```
    powershell -ExecutionPolicy ByPass -File .\deploy-minio.ps1
```
This deploys Minio, opens it in the browser and starts a processor pod
To login to Minio use the following credentials
User: test
PSW: test@123
After a while the JMeter output files should appear in Minio
## Stop and remove the deployement
```
    powershell -ExecutionPolicy ByPass -File .\delete-minio.ps1
```
