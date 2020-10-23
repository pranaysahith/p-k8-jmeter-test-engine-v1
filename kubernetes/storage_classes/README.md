## This folder contains the storage classes of persistent volumes

## Azure Kubernetes Service

`azure-file` storage class supports read/write from multiple pods. This means all pods of a deployment can use the same volume even though the pods are scheduled on different nodes in the cluster.

If this storage class is not the default storage class in the kubernetes cluster, we need to explicitly mention the storage class name in persistent volume claims.

Run the below one time command in the cluster to create the storage class:

`kubectl apply -f azure-file-storage.yaml`


## Elastic Kubernetes Service (AWS)

To be done.
