1:- Create a file named azure-file-storage.yaml for Storage Class declaration

2:- Create the storage class with the kubectl apply command:
    kubectl apply -f azure-file-storage.yaml

3:- Now create a file named azure-file-storage-pvc.yaml for persistent volume claim (PVC) uses the storage class object to dynamically provision.

4:- Create the persistent volume claim with the kubectl apply command:
    kubectl apply -f azure-file-storage-pvc.yaml

5:- Get the details of all pods by following command
    kubectl get all -n minio

6:- Get and edit files by following command
    kubectl describe deployment.apps/minio -n minio
    kubectl get deployment.apps/minio -n minio -o yaml > minio_deploy_original.yaml    

7:- Edit minio.yaml file and add volume mount and volume as show in file.

8:- apply changes with kubectl apply -f minio.yaml     
    kubectl apply -f minio_deploy.yaml 

            
