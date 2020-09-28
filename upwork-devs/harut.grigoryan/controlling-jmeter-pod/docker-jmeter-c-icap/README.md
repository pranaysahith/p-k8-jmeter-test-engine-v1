# ICAP+JMeter Dockerfile

## Minio
To setup Minio instances on the node run 
```
    kubectl apply -f minio.yaml
```
Find out the NodePort ports for accessing the Minio instances
```
   kubectl get svc
   NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORTTCP         25h
   .....
   input-queue-nodeport         NodePort    10.98.121.211   <none>        9000:30747/TCP   25h
   .....
   output-queue-nodeport        NodePort    10.98.36.7      <none>        9000:31555/TCP   25h
```
Find out the IP
```
    minikube IP
    192.168.99.120
```
With the IP and port values obtained as above access
- the input queue at http://192.168.99.120:30747/minio/login
- the output queues at http://192.168.99.120:31555/minio/login

Access Key: test
Secret Key: test@123

## Run The Script

- Build docker image: `docker build -t ggrig/jmeter-c-icap:1.0 . `
- Run docker image: `docker run -d ggrig/jmeter-c-icap:1.0`
- Deploy the pod in a minikube cluster `kubeclt apply -f processor-deployment.yaml`

The Docker executes icap.jmx that is started via launch.sh.
The results are uploaded to Minio output




