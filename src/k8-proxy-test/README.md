*** Run Proxy site test ***
- In order to run proxy site test clone the repo - https://github.com/filetrust/Icap-Test-Framework
- Navigate to p-k8-proxysite-test
- run docker build command 
```
docker build -t k8-proxysite-image .
```
- execute docker run command to run the image
``` 
docker run -it k8-proxysite-image
```
the current setup in image is for single user for test. 

will add more steps to update those details in script