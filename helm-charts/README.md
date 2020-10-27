# Helm Charts 

## Overview

* [common-resources](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/helm-charts/common-resources)
* [jmeter-testdata] - WIP

## Helm Installation

Refer to this [helm-v2](https://v2.helm.sh/docs/using_helm/#installing-helm)  for installation.

## Helm Permissions

```shell
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'      
helm init --service-account tiller --upgrade
```

## Build and publish base image 


```shell
$ docker build . -t glasswallsolutions/jmeter:5.3 -f Dockerfiles/jmeter-base
$ docker push glasswallsolutions/jmeter:5.3
```

## Build and publish testdata image


```shell
$ docker build . -t glasswallsolutions/jmeter-testdata -f Dockerfiles/jmeter-testdata 
$ docker push glasswallsolutions/jmeter-testdata
```
