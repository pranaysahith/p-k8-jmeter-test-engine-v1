**k8-jmeter-test-engine**

**Project brief**

**k8-jmeter-test-engine-v1**

A first version of the Kubernetes (K8) native application able to generate up to 100000 concurrent requests directly to the ICAP server using the c-icap client.

**Requirements:**

- Azure Cli installed - https://docs.microsoft.com/pl-pl/cli/azure/


**Create Azure Kubernetes Service**

- Define Variables - parameters for K8S Service in Azure
``` bash
$RESOURCEGROUPNAME="k8sk8s"
$LOCATION="eastus"
$AKS_NAME="k8s-test"
$NODES="1"
$MAXPODS="30"
```

- Deploy Azure Kubernetes Service
``` bash
az login
az account set --subscription subscrybtionid
az group create -l $LOCATION -n $RESOURCEGROUPNAME
az aks create --name $AKS_NAME --resource-group $RESOURCEGROUPNAME --node-count $NODES --generate-ssh-keys --network-plugin kubenet --max-pods $MAXPODS --enable-rbac --enable-managed-identity --vm-set-type VirtualMachineScaleSets --no-ssh-key
```

**Install kubeclt and connect to the AKS instance**

- Deploy Azure Kubernetes Service
``` bash
az aks install-cli
$env:path += 'C:\Users\admin\.azure-kubectl'
az aks get-credentials --resource-group $RESOURCEGROUPNAME --name $AKS_NAME
```

**Run Kubernetes Dashboard**

``` bash
kubectl delete clusterrolebinding kubernetes-dashboard
kubectl create clusterrolebinding kubernetes-dashboard --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard --user=clusterUser
kubectl config view --raw
az aks browse --resource-group $RESOURCEGROUPNAME --name $AKS_NAME
```
**Create secondary node pool dedicated to the JMeter workloads.**

``` bash
kubectl config view --raw
az aks browse --resource-group $RESOURCEGROUPNAME --name $AKS_NAME
az aks nodepool add --resource-group $RESOURCEGROUPNAME --cluster-name $AKS_NAME --name jmeter --node-count 1 --node-taints sku=jmeter:NoSchedule
```

**Test Deployemnt**

- Deploy to nodepool (default) 
``` bash
kubectl create -f akstest/phpinfo.yaml
kubectl get pods
kubectl get service
```
- Deploy to jmeter pool
``` bash
kubectl create -f akstest/phpinfojmeter.yaml
kubectl get pods
kubectl get service
```
- Destroy test deployment
``` bash
kubectldelete -f akstest/phpinfojmeter.yaml
kubectldelete -f akstest/phpinfo.yaml
kubectl get pods
kubectl get service
```


**Destroy Azure Kubernetes Service**

- Deploy to nodepool (default) 
``` bash
az group delete --name $RESOURCEGROUPNAME --yes --no-wait
```
