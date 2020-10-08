# ICAP+JMeter Dockerfile

## Minio
### Deploy Services
```
    powershell -ExecutionPolicy ByPass -File .\deploy-services.ps1
```
This deploys Minio and InfluxDB 

Minio can be accessed at `http://localhost:9000/`
InfluxDB at `http://localhost:8086/`

Minio credentials
User: test
PSW: test@123

Create a Minio backet called `input` and upload your test files there

## JMeter Jobs
### Run
On Windows 10 run the following from within the PowerShell
```
    powershell -ExecutionPolicy ByPass -File run.ps1 <file_list> <number_of_pods>
```
Where <file_list> is a text file containing the list of files to be handled during the test
The files are to be uploaded to the Minio `input` bucket prior to starting the test

So, to start 10 JMeter jobs run:
```
    powershell -ExecutionPolicy ByPass -File run.ps1 files.txt 10
```
### Stop and remove 
```
    powershell -ExecutionPolicy ByPass -File stop.ps1
```