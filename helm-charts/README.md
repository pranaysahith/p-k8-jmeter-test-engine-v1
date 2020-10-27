# Helm Charts 

## Overview

* [common-resources](https://github.com/k8-proxy/p-k8-jmeter-test-engine/tree/helm-charts/helm-charts/common-resources/)
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
