## secrets
All secrets are currently set to default value `admin`. Secrets can be created/viewed with below commands. Update [secrets-file]() if required.

Creating secret
```shell
$ echo -n 'admin' | base64
```

Decoding secret

```shell
echo 'YWRtaW4=' | base64 --decode
```

## Port Forwarding

### Grafana

```shell
$ kubectl port-forward -n common service/grafana-service 3000:80
```
### Minio

```shell
$ kubectl port-forward -n common service/minio-service 9000:80
```
### InfluxDB

```shell
kubectl port-forward -n common service/influxdb-service 3000:80
```
