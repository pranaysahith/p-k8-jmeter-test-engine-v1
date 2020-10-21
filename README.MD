**k8-jmeter-test-engine-v1**

A first version of the Kubernetes (K8) native application able to generate up to 100000 concurrent requests directly to the ICAP server using the c-icap client.

**Requirements:**

- Azure cli installed - https://docs.microsoft.com/pl-pl/cli/azure/

**Create Azure Kubernetes Service**

- Define Variables - parameters for K8S Service in Azure
``` bash
$RESOURCEGROUPNAME="k8sk8s"
$LOCATION="eastus"
$AKS_NAME="k8s-test"
$MONITORINGNODES="1"
$MAXPODS="70"
```

- Deploy Azure Kubernetes Service
``` bash
az login
az account set --subscription subscrybtionid
az group create -l $LOCATION -n $RESOURCEGROUPNAME
az aks create --name $AKS_NAME --resource-group $RESOURCEGROUPNAME --node-count $NODES --generate-ssh-keys --network-plugin kubenet --max-pods 1 --enable-rbac --enable-managed-identity --vm-set-type VirtualMachineScaleSets --no-ssh-key
```

- Deploy node pool dedicated to the monitoring/system workloads and delete the default one.
``` bash
az aks nodepool add --resource-group $RESOURCEGROUPNAME --cluster-name $AKS_NAME --name monitoring --node-count $MONITORINGNODES --node-taints sku=monitoring:NoSchedule
az aks nodepool update --resource-group $RESOURCEGROUPNAME --cluster-name $AKS_NAME --name monitoring --mode system
az aks nodepool delete --resource-group $RESOURCEGROUPNAME --cluster-name $AKS_NAME --name nodepool1
```

**Create a secondary node pool dedicated to the JMeter workloads.**

``` bash
$JMETERNODES="1"
az aks nodepool add --resource-group $RESOURCEGROUPNAME --cluster-name $AKS_NAME --name jmeter --node-count $JMETERNODES --node-taints sku=jmeter:NoSchedule
```

**Install kubeclt and connect to the AKS instance**

- Deploy Azure Kubernetes Service
``` bash
az aks install-cli
$env:path += 'C:\Users\admin\.azure-kubectl'
az aks get-credentials --resource-group $RESOURCEGROUPNAME --name $AKS_NAME
```

**Run Kubernetes Dashboard (optional)**

``` bash
kubectl delete clusterrolebinding kubernetes-dashboard
kubectl create clusterrolebinding kubernetes-dashboard --clusterrole=cluster-admin --serviceaccount=kube-system:kubernetes-dashboard --user=clusterUser
kubectl config view --raw
start-process -FilePath "az" -ArgumentList "aks browse --resource-group $RESOURCEGROUPNAME --name $AKS_NAME"
```


**Test Deployment**

- Deploy to nodepool (default) 
``` bash
kubectl create -f akstest/phpinfo.yaml
kubectl get pods -o wide
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
kubectl delete -f akstest/phpinfojmeter.yaml
kubectl delete -f akstest/phpinfo.yaml
kubectl get pods -o wide
kubectl get service
```
**Destroy Azure Kubernetes Service**

- Deploy to nodepool (default) 
``` bash
az group delete --name $RESOURCEGROUPNAME --yes --no-wait
```
