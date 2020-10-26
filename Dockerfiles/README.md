# DockerImages 

## Overview

* [jmeter-base](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/kubernetes/common_resources/grafana.yaml)
* [jmeter-testdata](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/kubernetes/common_resources/grafana.yaml)

## Build and Publish base image 


```shell
$ docker build . -t glasswallsolutions/jmeter:5.3
$ docker push glasswallsolutions/jmeter:5.3
```

## Build and publish testdata image


```shell
$ docker build . -t glasswallsolutions/jmeter-testdata -f Dockerfiles/jmeter-testdata 
$ docker push glasswallsolutions/jmeter-testdata
```
